# crawler with scrapy
import scrapy
from scrapy.crawler import CrawlerProcess

# lego item url: https://www.toys-for-fun.com/de/60139-mobile-einsatzzentrale.html
# lego category url: https://www.toys-for-fun.com/de/kategorien/bauen-konstruieren/lego/duplo.html

class SpiderToysForFun(scrapy.Spider):
    name = 'test'
    allowed_domains = ["www.toys-for-fun.com"]
    start_urls = ['https://www.toys-for-fun.com/de/kategorien/bauen-konstruieren/lego/duplo.html']
    # start_urls = ['https://www.toys-for-fun.com/de/legor-duplor-10931-bagger-und-laster.html']

    def parse(self, response):
        class_tag = '.product-info'
        for product_info in response.css(class_tag):
            yield {
                'article': product_info.css('.product-name ::text').extract_first(),
                'price': convert_prices(product_info.css('.price ::text').extract_first()),  # clean later?
            }

    
def convert_prices(parsedPrice):
    if type(parsedPrice) == str:
        parsedPrice = parsedPrice.replace(',', '.')
        for char in ['\n', '\xa0', '€']:
            parsedPrice = parsedPrice.replace(char, '')
    return float(parsedPrice)

if __name__ == '__main__':
    process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(SpiderToysForFun)
    process.start()
