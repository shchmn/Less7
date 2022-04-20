import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from castorama.items import CastoramaItem


class CrruSpider(scrapy.Spider):
    name = 'crruv'
    allowed_domains = ['castorama.ru']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.category = None
        self.start_urls = [f"https://www.castorama.ru/catalogsearch/result/?q={kwargs.get('query')}"]

    def parse(self, response: HtmlResponse):
        self.category = response.xpath("//h1/text()")

        next_page = response.xpath("//a[@class='next i-next']")
        if next_page:
            yield response.follow(next_page[0], callback=self.parse)

        links = response.xpath("//a[@class='product-card__img-link']")
        for link in links:
            yield response.follow(link, callback=self.castorama_parse)

    def castorama_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoramaItem(), response=response)
        loader.add_xpath('name', '//h1[contains(@class, "product-essential__name")]/text()')
        loader.add_xpath('price', '//span[@xpath="1"]/text()')
        loader.add_xpath('photos', "//img[contains(@class, 'top-slide__img')]/@data-src")
        loader.add_value('url', response.url)

        yield loader.load_item()
