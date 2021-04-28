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

    video_id = 0
    citation_id = 0

    def open_spider(self, spider):
        self.file_video = open('db/videos.jsonl', 'w', encoding='utf-8')
        self.file_citation = open('db/citations.jsonl', 'w', encoding='utf-8')
        self.file_video_citation = open('db/video_citation.jsonl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file_video.close()
        self.file_citation.close()
        self.file_video_citation.close()

    def process_item(self, item, spider):
        if isinstance(item, VideoItem):
            self.video_id += 1
            return self.handleVideo(item, spider)
        if isinstance(item, CiteItem):
            self.citation_id += 1
            return self.handleCitation(item, spider)

    def handleVideo(self, item, spider):
        item['id'] = self.video_id
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

        if len(urllist[-1]) == 0:
            pmid = urllist[-2]
        else:
            pmid = urllist[-1]
        
        if not pmid.isnumeric():
            pmcid = pmid
            pmid = ""

        if not pmcid.startswith("PMC"):
            pmcid = ""

        # line_txt = f"PMID:{pmid}\nPMCID:{pmcid}\nAU:{authors}\nTI:{title}\nJO:{journal}\nDP:{datep}\nVL:{vol}\nPG:{pages}\nURL:{url}\nVURL:{video_url}\nCI:{item['citation']}\n\n"

        item['id'] = self.citation_id
        item['pmid'] = pmid
        item['pmcid'] = pmcid
        item['authors'] = authors
        item['title'] = title
        item['journal'] = journal
        item['date'] = datep
        item['volume'] = vol
        item['pages'] = pages

        line_json = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
        line_video_citation = json.dumps({"id": self.citation_id, "video_url": video_url, "citation_url": url}, ensure_ascii=False) + "\n"

        self.file_citation.write(line_json)
        self.file_video_citation.write(line_video_citation)

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