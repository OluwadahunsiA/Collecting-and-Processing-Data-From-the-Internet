# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from pymongo import MongoClient
from uri import uri
from scrapy.pipelines.images import ImagesPipeline


class InstagramPipeline:
    def process_item(self, item, spider):
        return item

    
class InstagramPipeline:
    def __init__(self):
        client = MongoClient(uri, 27017)
        self.mongo = client['instagram']

    def process_item(self, item, spider):
        collection = self.mongo[spider.name]
        collection.insert_one(item)
        return item

class InstagramPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['picture_follows']:
            try:
                yield scrapy.Request(item['picture_follows'])
            except Exception as e:
                print(e)