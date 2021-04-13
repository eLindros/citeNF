# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class VideoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    video = scrapy.Field()
    title = scrapy.Field()
    transcript = scrapy.Field()
    keywords = scrapy.Field()

class CiteItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    video_url = scrapy.Field()
    video_title = scrapy.Field()
    video_keywords = scrapy.Field()