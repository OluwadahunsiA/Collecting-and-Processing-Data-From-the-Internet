# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from uri import uri
from scrapy.pipelines.images import ImagesPipeline


class ProductsPipeline:
    
    def __init__(self):
        client = MongoClient(uri, 27017)
        self.mongo = client['goods']
        
    def process_item(self, item, spider):
        item['characteristics'] = dict(zip(item['characteristics_keys'], item['characteristics_values']))
        del item['characteristics_keys']
        del item['characteristics_values']
        
        collection = self.mongo[spider.name]
        collection.update_one(item, {'$set':item},upsert=True)
        return item

class ProductsImagesPipeline(ImagesPipeline):
    def get_media_requests(self,item,info):
        if item['images']:
            for image in item['images']:
                try:
                    yield scrapy.Request(image)
                except Exception as err:
                    print(err)
        return item
    
    def item_completed(self, results,item,info):
        if results:
            item['images'] = [i[1] for i in results if i[0]]
        return item