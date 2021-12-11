import scrapy
from bearspace.items import BearspaceItem

class BearspaceSpider(scrapy.Spider):
    name = "bearspace"
    #since its a WIX based website, wont bother crawling internal XHR requests
    url_schema = "https://www.bearspace.co.uk/purchase?page={0}" 
    #or https://www.bearspace.co.uk/purchase?page=100 to get all in 1 request
    page = 1
    
    def start_requests(self):
        yield scrapy.Request(url=self.url_schema.format(self.page))

    def parse(self, response):
        urls = response.css('[data-hook="product-item-root"] a').xpath('@href').extract()
        for url in urls:
            yield scrapy.Request(url = url, callback=self.parse_artwork)

        #if more button then paginate
        more_prods_check = response.css('[data-hook="load-more-button"]')
        if more_prods_check:
            self.page+=1
            yield response.follow(url = self.url_schema.format(self.page))

    def parse_artwork(self, response):
        item = BearspaceItem()
        item['url'] = response.url
        item['title'] = response.css('h1[data-hook="product-title"]').xpath('text()').extract_first()
        description_selector = response.css('[data-hook="description"] p').xpath('normalize-space(string())') or response.css('[data-hook="description"]').xpath('text()')
        media = description_selector.re('(.*[Ss]culpt.*|.*[Pp]aint.*|.*[Cc]anvas.*|.*[Pp]ortrait.*|.*[Cc]asting.*|.*[Cc]oloured.*|.*[Pp]rint.*|.*[Aa]crylic.*|.*[Mm]edia.*|.*[Ww]ood.*|.*[Gg]raphite.*|.*[Pp]encil.*)')
        height = description_selector.re(r'(?<![Xx|by])\d+\.*\d*(?=\s*c*m*\s*[Xx|by])')
        width = description_selector.re(r'(?<=[Xx|by|width])\s*\d+\.*\d*')
        item['media'] = media[0] if len(media) > 0 else media
        item['height_cm'] = height[0] if len(height) > 0 else height
        item['width_cm'] = width[0] if len(width) > 0 else width
        item['price_gbp'] = response.css('[property="product:price:amount"]').xpath('@content').extract_first()
        yield item
