import scrapy
from scrapy.loader import ItemLoader
import w3lib.html as wh
from citeNF.items import videoItem, citeItem

class NutrittionSpider(scrapy.Spider):
    name = "cite_spider"

    start_urls = ['https://nutritionfacts.org/video/flashback-friday-do-vitamin-d-supplements-help-with-diabetes-weight-loss-and-blood-pressure/']

    def parse (self, response):
        URL = self.start_urls[0]
        VIDEO_TITLE = response.xpath('//head/title/text()').get()
        TRANSCRIPT = wh.remove_tags(response.xpath('//div[@id="collapseTranscript"]/div').get())

        video = ItemLoader(item=videoItem(), response=response)

        video.add_value('url', URL)
        video.add_value('title', VIDEO_TITLE)
        video.add_xpath('video', '//meta[@property="og:video"]/@content')
        video.add_value('transcript', TRANSCRIPT)


        CITATION_SELECTOR = '//cite/a'

        yield video.load_item()

        for citation in response.xpath(CITATION_SELECTOR):
            c = ItemLoader(item=citeItem(), selector=citation)
            c.add_xpath('title', '@title')
            c.add_xpath('url', '@href')
            c.add_value('video_url', URL)
            c.add_value('video_title', VIDEO_TITLE)
           
            yield c.load_item()

        # next_page = response.xpath('//div[@class="previous-video"]/a/@href')
        
        # if next_page is not None:
           # yield response.follow(next_page, callback=self.parse)
