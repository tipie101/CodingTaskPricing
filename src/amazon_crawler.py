# There is an amazon-search API: https://webservices.amazon.com/paapi5/documentation/search-items.html
# However, to use it one needs the credentials of a fully accepted Amazon Associate

# Ausgangspunkt ist das Suchergebnis von Amazon:

# looking for: <a class="a-size-base a-link-normal a-text-normal" href="/LEGO-...-41343-.../"
# price is already given via next tag:
# <span class="a-price" data-a-size="l" data-a-color="base"><span class="a-offscreen">32,09 €</span><span aria-hidden="true"><span class="a-price-whole">32,09</span><span class="a-price-symbol">€</span></span></span>
# click on the link to find out if amazon is selling!
# look at <div id="merchant-info"> "Verkauf und Versnad durch Amazon" - perfekt!!!
# id="price_inside_buybox"

import pickle
import re
import scrapy
from scrapy.crawler import CrawlerProcess


amazon_search = []
lego_articles = [
    {'article_nr': '21129', 'subbrand': 'Minecraft'},
    {'article_nr': '42111', 'subbrand': 'Technic'},
    {'article_nr': '21153', 'subbrand': 'Minecraft'},
]
art = lego_articles[0]

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
                print(href)
                # TODO: Go deeper :D
                yield scrapy.Request(
                    response.urljoin(href),
                    callback=self.parse_sublink
                )

    def parse_sublink(self, response):
        print('reached sublink - single article view')


if __name__ == '__main__':
    process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    # SpiderToysffLego.set_subbrand('city')
    process.crawl(AmazonLegoSpider)
    process.start()
