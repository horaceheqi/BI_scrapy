# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CoolscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HuxiuItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    link = scrapy.Field()  # 链接
    desc = scrapy.Field()  # 简述
    posttime = scrapy.Field()  # 发布时间


class MessageItem(scrapy.Item):
    id = scrapy.Field()  # ID
    content = scrapy.Field()  # 信件内容


class UserItem(scrapy.Item):
    id = scrapy.Field()  # 会员ID
    regip = scrapy.Field()  # 注册IP
    loginip = scrapy.Field()  # 登陆IP


class TopicItem(scrapy.Item):
    topic = scrapy.Field()
    link = scrapy.Field()
    userid = scrapy.Field()
    replier = scrapy.Field()
