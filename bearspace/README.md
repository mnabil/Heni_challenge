# Bearspace Scrapy Spider

Bearspace is a spider for bearspace.co.uk/purchase

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install using Python 3.9+

```bash
#git clone and make a virtualenv (preferably)
cd bearspace && pip install -r requirements.txt
```

## Run
```bash
#to make sure code is syntactically and semantically correct
scrapy check
```

```bash
scrapy crawl bearspace --logfile bear.log -o bear.csv
```

## Contributing
Pull requests are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)