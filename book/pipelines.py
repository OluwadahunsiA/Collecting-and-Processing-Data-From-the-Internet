# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from uri import uri


class BookPipeline:
    
    def __init__(self):
        client = MongoClient(uri, 27017)
        self.mongo = client['books']
        
    def process_item(self, item, spider):
        item['price'] = float(item['price'])
        item['discount_price'] = float(item['discount_price'])
        item['book_rate'] = float(item['book_rate'])
        
        collection = self.mongo[spider.name]
        collection.insert_one(item)
        
        return item
