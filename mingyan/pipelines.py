# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from mingyan.topicitem import TopicItem, ReplierItem
import os
import time
import csv


class CsvFilePipeline(object):
    def __init__(self):
        # csv文件的位置,无需事先创建
        datatime = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
        store_file = os.path.dirname(__file__) + '/csvout/qtw_' + datatime + '.csv'
        # csv写法
        self.file = open(store_file, 'w', encoding='utf-8',newline='')
        self.csvwriter = csv.writer(self.file, delimiter=',',quoting=csv.QUOTE_NONNUMERIC)
        self.csvwriter.writerow(('主题', '回复用户', '回复内容'))

    def process_item(self, item, spider):
        if isinstance(item, TopicItem):
            pass
        if isinstance(item, ReplierItem):
            item['topic'] = item['topic'].replace("\n", "").replace("\r", "")
            item['content'] = item['content'].replace("\n", "").replace("\r", "")
            item['userid'] = item['userid'].replace("\n", "").replace("\r", "")
            topic = item['topic']
            content = item['content']
            userid = item['userid']
            self.csvwriter.writerow((topic, userid, content))
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()
