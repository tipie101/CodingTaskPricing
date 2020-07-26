# crawler with scrapy
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

#    'dc-super-hero-girls', 'legor-sonstige', 
#    'legor-brickheadz', 'legor-boost', 'legor-special-edition-sets', 'legor-ostern', 
#    'legor-jurassic-worldtm', 'legor-harry-pottertm', 'legor-froehliche-steinachten', 
#    'legor-4', 'legor-overwatch', 'legor-hidden-sidetm', 'legor-dotstm'

results = []

# lego item url: https://www.toys-for-fun.com/de/60139-mobile-einsatzzentrale.html
# lego category url: https://www.toys-for-fun.com/de/kategorien/bauen-konstruieren/lego/duplo.html

# used for 
class SpiderToysffLego(scrapy.Spider):
    name = 'test'
    allowed_domains = ["www.toys-for-fun.com"]

    start_urls = [
        # using exactly one url in order to gather all and only all products in the store of a given subbrand
        ''.join([base_url, brand, '.html']) for brand in subbrands
    ]

    # def set_subbrand(self, brand):
    #    self.subbrand = brand
    #    self.start_urls[0] = ''.join([self.base_url, self.subbrand, '.html'])

    def parse(self, response):
        class_tag = '.product-info'
        for product in response.css(class_tag):
            result = extract_product_info(product.css('.product-name ::text').extract_first())
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
    

if __name__ == '__main__':
    process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    # SpiderToysffLego.set_subbrand('city')
    process.crawl(SpiderToysffLego)
    process.start()
    pickle.dump(results, open( "./data/toysff.p", "wb" ))
