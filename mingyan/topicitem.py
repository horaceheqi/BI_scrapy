#!/usr/bin/env python
# -*- coding:utf-8 -*
from scrapy import Item, Field


class TopicItem(Item):
    topic = Field()
    userid = Field()
    replier = Field()
    url = Field()


class ReplierItem(Item):
    topic = Field()
    userid = Field()
    content = Field()
