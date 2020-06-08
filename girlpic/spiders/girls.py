# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from girlpic.items import GirlpicItem

class GirlsSpider(CrawlSpider):
    name = 'girls'
    allowed_domains = ['girlsky.cn']
    start_urls = ['http://www.girlsky.cn']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[3]/div[3]/ul/li/a'),
             callback='parse_image', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="ArticleId8"]/div[1]/a', deny='.*/\d*\.html'),
             callback='parse_image', follow=True)
    )

    def parse_image(self, response):
        url = response.urljoin(response.xpath('//*[@id="ArticleId8"]/div[1]/a/img/@src').get())
        # 使用ImagesPipeline时urls必须用列表
        urls = []
        urls.append(url)
        title = response.xpath('/html/body/div[2]/div[2]/h1/text()').get().split('(')[0]
        item = GirlpicItem(image_urls=urls, title=title)
        yield item

