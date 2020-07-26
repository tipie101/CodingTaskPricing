# There is an amazon-search API: https://webservices.amazon.com/paapi5/documentation/search-items.html
# However, to use it one needs the credentials of a fully accepted Amazon Associate

# looking for: <a class="a-size-base a-link-normal a-text-normal" href="/LEGO-...-41343-.../"
# price is already given via next tag:
# <span class="a-price" data-a-size="l" data-a-color="base"><span class="a-offscreen">32,09 €</span><span aria-hidden="true"><span class="a-price-whole">32,09</span><span class="a-price-symbol">€</span></span></span>
# click on the link to find out if amazon is selling!
# look at <div id="merchant-info"> "Verkauf und Versnad durch Amazon" - perfekt!!!
# id="price_inside_buybox"

import lego_pricing_crawler  # TODO: utils bib!
import pandas as pd
import pickle
import re
import scrapy
from scrapy.crawler import CrawlerProcess


amazon_search = []
# load from pickle
lego_articles = pickle.load(open('./data/toysff.p', 'rb'))
results = []
original = 'Verkauf und Versand durch Amazon.'

class AmazonLegoSpider(scrapy.Spider):
    # a crawler to collect search result links
    name = 'amazon_lego_prices'
    start_urls = [
        '+'.join(['https://www.amazon.de/s?k=lego', art['subbrand'], art['article_nr']]) 
        for art in lego_articles
    ]

    def parse(self, response):
        for href in response.css("a::attr(href)").extract():
            if re.search('^/LEGO(%C2%AE)?-', href) and any('-' + art['article_nr'] + '-' in href for art in lego_articles):
                yield scrapy.Request(
                    response.urljoin(href),
                    callback=self.parse_sublink
                )

    def parse_sublink(self, response):
        print('reached sublink - single article view')
        if response.css('#merchant-info::text') and original in response.css('#merchant-info::text').extract_first():
            info = response.request.url.split('/')[3]     
            article_nr = re.findall(r"\D(\d{5})\D", info)[0]
            price = lego_pricing_crawler.convert_price(response.css("#price_inside_buybox::text").extract_first())
            result = {'brand': 'LEGO', 'article_nr': article_nr, 'name': info, 'price': price}
            results.append(result)
            yield result

def crawl():
    process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(AmazonLegoSpider)
    process.start()
    pickle.dump(results, open( "./data/amazon.p", "wb" ))


if __name__ == '__main__':
    crawl()
