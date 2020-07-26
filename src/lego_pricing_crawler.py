# crawler for lego articles of toys-for-fun.com

import pickle
import re
import scrapy
from scrapy.crawler import CrawlerProcess


base_url = 'https://www.toys-for-fun.com/de/kategorien/bauen-konstruieren/lego/'
subbrands = [
    'juniors','duplo', 'classic','creator','disney-princess','friends','city','nexo-knights', 
    'architecture', 'castle', 'dc-comic-super-heroes', 'exclusive-sets', 'legends-of-chima', 
    'movie', 'marvel-super-heroes', 'mindstorms', 'mixels', 'ninjago', 'star-wars', 'technic', 
    'teenage-mutant-ninja-turtles', 'ultra-agents', 'bionicle', 'elves', 'pirates', 
    'speed-champions', 'minifiguren', 'minecraft'
]
results = []
# lego category url: https://www.toys-for-fun.com/de/kategorien/bauen-konstruieren/lego/duplo.html

class SpiderToysffLego(scrapy.Spider):
    name = 'test'
    allowed_domains = ["www.toys-for-fun.com"]

    start_urls = [
        # using exactly one url for each subbrand
        ''.join([base_url, brand, '.html']) for brand in subbrands
    ]


    def parse(self, response):
        class_tag = '.product-info'
        for product in response.css(class_tag):
            result = extract_product_info(product.css('.product-name ::text').extract_first())
            # Choose special-price instead of the old one
            if product.css('.special-price'):
                result['price'] = convert_price(product.css('.special-price .price ::text').extract_first())
            else:
                result['price'] = convert_price(product.css('.price ::text').extract_first())
            results.append(result)
            yield result


def convert_price(parsed_price):
    if type(parsed_price) == str:
        parsed_price = parsed_price.replace(',', '.')
        for char in ['\n', '\xa0', '€']:
            parsed_price = parsed_price.replace(char, '')
        return float(parsed_price.strip())
        
    return float(parsed_price)


def extract_product_info(info):
    if type(info) != str:
        return None
    digits = re.findall(r" (\d{5}) ", info)
    if len(digits) != 1:
        return None
    art_nr = digits[0]
    split = info.split(art_nr)
    return {
        'brand': 'LEGO',
        'subbrand': split[0].replace('LEGO® ', '').replace('™', ''),
        'article_nr': art_nr.strip(),
        'name': split[1]
    }


def crawl():
    process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(SpiderToysffLego)
    process.start()
    pickle.dump(results, open( "./data/toysff.p", "wb" ))


if __name__ == '__main__':
    crawl()
