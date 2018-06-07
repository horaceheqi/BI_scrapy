#!/usr/bin/env python
# -*- coding:utf-8 -*
import scrapy
from scrapy import Request
from scrapy import Selector
from mingyan.topicitem import TopicItem, ReplierItem


class NGASpider(scrapy.Spider):
    name = "ngaspider"
    host = "https://bbs.hupu.com"
    start_urls = [
        "https://bbs.hupu.com/pubg"
    ]

    def parse(self, response):
        pass

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        content_list = response.xpath("//*[@class='show-list']/ul/li")
        for content in content_list:  # tr
            topicItem = TopicItem()
            topicItem['topic'] = ','.join(content.xpath('div[1]/a').xpath('string(.)').extract())  # td
            topicItem['userid'] = ','.join(content.xpath('div[2]/a').xpath('string(.)').extract())  # td
            topicItem['replier'] = ','.join(content.xpath('div[3]/a').xpath('string(.)').extract())  # td

            url = self.host + content.xpath('div[1]/a[1]/@href').extract_first()
            topicItem['url'] = url
            yield Request(url=url, meta={'topic': topicItem['topic']}, callback=self.parse_topic)

    def parse_topic(self, response):
        topic = response.meta.get('topic')
        content_list = response.xpath("//*[@id='readfloor']/div[@class='floor']")
        for content in content_list:
            replier = ReplierItem()
            replier['topic'] = topic
            replier['userid'] = content.xpath("div[@class='floor_box']/div[@class='author']//a/text()").extract_first()
            replier['content'] = content.xpath("div[@class='floor_box']/table[@class='case']").xpath('string(.)').extract_first()
            yield replier

