
import scrapy
from scrapy.http import HtmlResponse

from book.items import BookItem

class BookSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['www.labirint.ru']
    start_urls = ['https://www.labirint.ru/search/python/?stype=0']
    
    
    def parse(self,response:HtmlResponse):
        next_page_link = response.xpath("//div[contains(@class, 'pagination-next-mobile')]/a[@class='pagination-next__text']/@href").extract_first()
        
        if next_page_link:
            yield response.follow(next_page_link, self.parse)
        
        links = response.xpath("//div[@data-position]//a[@class='product-title-link']/@href").extract()
        
        for link in links:
            yield response.follow(link,self.parse_book)
            
    
    def parse_book(self,response:HtmlResponse):
        link = response.url
        name = response.xpath("//div[@id='product-info']/@data-name").extract_first()
        authors = response.xpath("a[@data-event-label = 'author']/@data-event-content").extract()
        price = response.xpath("//div[@id='product-info']//@data-price").extract_first()
        discount_price = response.xpath("//div[@id='product-info']//@data-discount-price").extract_first()
        availability = response.xpath("//div[@id = 'product-info']/@data-available-status").extract_first()
        rate = response.xpath("//div[@id='product-info']/@data-available-status").extract_first()
        
        
        yield BookItem(link = link, name = name, authors = authors, price = price, discount_price = discount_price, availability = availability ,rate = rate)