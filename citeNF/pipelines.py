# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from citeNF.items import VideoItem, CiteItem
import json

class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file_video = open('videos.jsonl', 'a', encoding='utf-8')
        self.file_citation_jsonl = open('citation.jsonl', 'a', encoding='utf-8')
        self.file_citation_txt = open('citation.txt', 'a', encoding='utf-8')

    def close_spider(self, spider):
        self.file_video.close()
        self.file_citation_jsonl.close()
        self.file_citation_txt.close()

    def process_item(self, item, spider):
        if isinstance(item, VideoItem):
            return self.handleVideo(item, spider)
        if isinstance(item, CiteItem):
            return self.handleCitation(item, spider)

    def handleVideo(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
        self.file_video.write(line)
        return item

    def handleCitation(self, item, spider):
        citation = item['citation'].split(".")
        authors = citation[0]
        title = citation[1].strip()
        journal = citation[2].strip()
        rest = citation[3].split(";")
        datep = rest[0].strip()
        vol_pages= rest[-1].split(":")
        vol = vol_pages[0].strip()
        pages = vol_pages[-1].strip()
        url = item['url']
        urllist = url.split("/")
        pmcid = ""
        video_url = item['video_url']
        video_title = item['video_title']

        if len(urllist[-1]) == 0:
            pmid = urllist[-2]
        else:
            pmid = urllist[-1]
        
        if not pmid.isnumeric():
            pmcid = pmid
            pmid = ""

        if not pmcid.startswith("PMC"):
            pmcid = ""

        line_txt = f"PMID:{pmid}\nPMCID:{pmcid}\nAU:{authors}\nTI:{title}\nJO:{journal}\nDP:{datep}\nVL:{vol}\nPG:{pages}\nURL:{url}\nVURL:{video_url}\nVTIT:{video_title}\nCI:{item['citation']}\n\n"

        item['pmid'] = pmid
        item['pmcid'] = pmcid
        item['authors'] = authors
        item['title'] = title
        item['journal'] = journal
        item['date'] = datep
        item['volume'] = vol
        item['pages'] = pages

        line_json = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"

        self.file_citation_jsonl.write(line_json)
        self.file_citation_txt.write(line_txt)

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