import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from twisted.internet import reactor



from products.items import ProductsItem


class LeroyMerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['www.leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/keramicheskaya-plitka/']
    
    def parse(self,response:HtmlResponse):
        next_page_link = response.xpath("//a[contains(@aria-label, 'Следующая страница:')]/@href").extract_first()
        
        if next_page_link:
            yield response.follow(next_page_link,self.parse)
            
        links = response.xpath("//div[@data-qa-product]/a/@href").extract()
        
        for link in links:
            yield response.follow(link,self.good_parse)
            
    def good_parse(self,response:HtmlResponse):
        loader = ItemLoader(item=GoodsparserItem(), response = response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('images','//picture[@slot="pictures"]/source[contains(@data-origin,"2000")]/@data-origin')
        loader.add_xpath('characteristics_keys','//dl/div/dt/text()')
        loader.add_xpath('characteristics_values','//d1/div/dd/text()')
        loader.add_value('link', response.url)
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        
        yield loader.load_item()