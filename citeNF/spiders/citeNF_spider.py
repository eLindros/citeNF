import scrapy
from scrapy.loader import ItemLoader
import w3lib.html as wh
from citeNF.items import VideoItem, CiteItem

class NutrittionSpider(scrapy.Spider):
    name = "cite_spider"
    start_urls = ['https://nutritionfacts.org/video/heart-stents-and-upcoding-how-cardiologists-game-the-system/']

    def __init__(self):
        self.i = 1

    def parse (self, response):
        URL = self.start_urls[0]
        VIDEO_TITLE = response.xpath('//head/title/text()').get()
        VIDEO_URL = response.xpath('//meta[@property="og:video"]/@content').get()
        TRANSCRIPT = wh.remove_tags(response.xpath('//div[@id="collapseTranscript"]/div').get())

        video = VideoItem()

        video['url'] = URL
        video['title'] = VIDEO_TITLE
        video['video'] = VIDEO_URL
        video['transcript'] = TRANSCRIPT

        yield video


        CITATION_SELECTOR = '//cite/a'

        for citation in response.xpath(CITATION_SELECTOR):
            cItem = CiteItem()

            cItem['title'] = citation.xpath('@title').get()
            cItem['url'] = citation.xpath('@href').get()
            cItem['video_url'] = URL
            cItem['video_title'] = VIDEO_TITLE
           
            yield cItem

        next_page = response.xpath('//div[@class="previous-video"]/a/@href').get()
        
        if next_page is not None and self.i < 3:
            self.i += 1
            yield response.follow(next_page, callback=self.parse)
