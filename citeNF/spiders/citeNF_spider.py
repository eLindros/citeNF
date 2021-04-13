import scrapy
from scrapy.loader import ItemLoader
import w3lib.html as wh
from citeNF.items import VideoItem, CiteItem

class NutrittionSpider(scrapy.Spider):
    name = "cite_spider"
    start_urls = ['https://nutritionfacts.org/video/heart-stents-and-upcoding-how-cardiologists-game-the-system/']
    next_page = start_urls[0]

    def parse (self, response):
        URL = self.next_page
        VIDEO_TITLE = response.xpath('//head/title/text()').get()
        VIDEO_URL = response.xpath('//meta[@property="og:video"]/@content').get()
        TRANSCRIPT = wh.remove_tags(response.xpath('//div[@id="collapseTranscript"]/div').get())
        KEYWORDS = response.xpath('//ul[@class="list-inline video-topics"]/li/a/text()').getall()

        video = VideoItem()

        video['url'] = URL
        video['title'] = VIDEO_TITLE
        video['video'] = VIDEO_URL
        video['transcript'] = TRANSCRIPT
        video['keywords'] = KEYWORDS

        yield video

        CITATION_SELECTOR = '//cite/a'

        for citation in response.xpath(CITATION_SELECTOR):
            cItem = CiteItem()

            cItem['title'] = citation.xpath('@title').get()
            cItem['url'] = citation.xpath('@href').get()
            cItem['video_url'] = URL
            cItem['video_title'] = VIDEO_TITLE
            cItem['video_keywords'] = KEYWORDS
           
            yield cItem

        self.next_page = response.xpath('//div[@class="previous-video"]/a/@href').get()
        
        if self.next_page is not None:
            pass
#            yield response.follow(self.next_page, callback=self.parse)
