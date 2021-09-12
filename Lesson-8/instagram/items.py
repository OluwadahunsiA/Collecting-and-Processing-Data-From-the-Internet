# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def process_int(value):
    try:
        value = int(value)
        return value
    except:
        return value

class InstagramItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field(input_processor=MapCompose(process_int))
    follow_id = scrapy.Field(input_processor=MapCompose(process_int))
    follow_name = scrapy.Field()
    follow_fullname = scrapy.Field()
    pic_follow = scrapy.Field()
    _id = scrapy.Field()
   
