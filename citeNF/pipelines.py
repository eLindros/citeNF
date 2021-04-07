# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from citeNF.items import videoItem, citeItem
import json


class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file_video = open('videos.jl', 'w', encoding='utf-8')
        self.file_citation = open('citation.jl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file_video.close()
        self.file_citation.close()

    def process_item(self, item, spider):
        if isinstance(item, videoItem):
            return self.handleVideo(item, spider)
        if isinstance(item, citeItem):
            return self.handleCitation(item, spider)

    def handleVideo(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
        self.file_video.write(line)
        return item

    def handleCitation(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
        self.file_citation.write(line)
        return item


class DuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['url'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter['url'])
            return item