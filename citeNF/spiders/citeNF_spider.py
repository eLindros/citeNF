import scrapy
from scrapy.loader import ItemLoader
import w3lib.html as wh
from citeNF.items import VideoItem, CiteItem

class NutrittionSpider(scrapy.Spider):
    name = "cite_spider"
    # start_urls = ['https://nutritionfacts.org/video/preventing-inflammatory-bowel-disease-with-diet/']
    start_urls = ['https://nutritionfacts.org/video/kombuchas-side-effects-is-it-bad-for-you/']
    next_page = start_urls[0]

    def parse (self, response):
        URL = self.next_page
        VIDEO_TITLE = response.xpath('//head/title/text()').get()
        VIDEO_URL = response.xpath('//meta[@property="og:video"]/@content').get()
        TRANSCRIPT = wh.remove_tags(response.xpath('//div[@id="collapseTranscript"]/div').get())
        KEYWORDS = response.xpath('//ul[@class="list-inline video-topics"]/li/a/text()').getall()
        NEXT_VIDEO = response.xpath('//div[@class="next-video"]/a/@href').get()
        PREV_VIDEO = response.xpath('//div[@class="previous-video"]/a/@href').get()
        DATE = response.xpath('//time/@datetime').get()

        video = VideoItem()

        video['url'] = URL
        video['title'] = VIDEO_TITLE
        video['video'] = VIDEO_URL
        video['transcript'] = TRANSCRIPT.replace('\t','').replace('#', '').replace('\n', '\n\n')
        video['keywords'] = KEYWORDS
        video['next_video'] = NEXT_VIDEO
        video['prev_video'] = PREV_VIDEO
        video['date'] = DATE

        yield video


        CITATION_SELECTOR = '//cite/a'

        for citation in response.xpath(CITATION_SELECTOR):
            cItem = CiteItem()

            cItem['citation'] = citation.xpath('@title').get()
            cItem['url'] = citation.xpath('@href').get()
            cItem['video_url'] = URL
           
            yield cItem

        self.next_page = NEXT_VIDEO
        
        if self.next_page is not None:
            yield response.follow(self.next_page, callback=self.parse)
            # pass