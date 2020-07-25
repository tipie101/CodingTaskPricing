# crawler with scrapy
import pickle
import scrapy
from scrapy.crawler import CrawlerProcess


base_url = 'https://www.toys-for-fun.com/de/kategorien/bauen-konstruieren/lego/'
subbrands = [
    'architecture', 'bionicle', 'duplo', 'city', 'juniors', 'classic', 'disney-princess',
    'friends', 'elves', 'speed-champions', 'star-wars', 'movie', 'technic'
]
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
    split = info.split()
    return {
        'brand': split[0].replace('®', ''),
        'subbrand': split[1].replace('®', ''),
        'article_nr': split[2],
        'name': " ".join(split[3:])
    }
    

if __name__ == '__main__':
    process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    # SpiderToysffLego.set_subbrand('city')
    process.crawl(SpiderToysffLego)
    process.start()
    pickle.dump(results, open( "./data/toysff.p", "wb" ))
