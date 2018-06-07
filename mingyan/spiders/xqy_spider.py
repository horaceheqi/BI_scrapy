#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 绣球缘
Desc : 模拟登录http://www.8181.com.cn/admincp.php后将用户列表和站内信全部爬出来
tips：使用chrome调试post表单的时候勾选Preserve log和Disable cache
"""
import logging
import re
import os
import sys
import time
import json

import scrapy
from scrapy.http import Request

from mingyan.items import MessageItem, UserItem

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler(sys.stdout)])


class XqySpider(scrapy.Spider):
    name = "xqy"
    # allowed_domains = ["www.8181.com.cn"]
    start_urls = [
        # 'https://www.8181.com.cn/admincp.php?c=user',
        # 'https://www.8181.com.cn/admincp.php?c=message',
        'file:///D:/Learning/Scrapy/%E9%A1%B5%E9%9D%A2%E5%88%86%E6%9E%90/%E4%BC%9A%E5%91%98%E7%AE%A1%E7%90%86.html',
        'file:///D:/Learning/Scrapy/%E9%A1%B5%E9%9D%A2%E5%88%86%E6%9E%90/%E4%BF%A1%E4%BB%B6%E7%AE%A1%E7%90%86.html',
    ]

    # user_url = 'http://www.8181.com.cn/admincp.php?c=user&a=view&fromtype=jdbox&id={}&r=LMH3QE&keepThis=true&'
    # message_url = 'http://www.8181.com.cn/admincp.php?c=message&a=edit&id={}&fromtype=jdbox&r=P3KY9Y&keepThis=true&'
    user_url = 'file:///D:/Learning/Scrapy/%E9%A1%B5%E9%9D%A2%E5%88%86%E6%9E%90/%E4%BC%9A%E5%91%98%E7%AE%A1%E7%90%86_%E8%AF%A6%E6%83%85.html'
    message_url = 'file:///D:/Learning/Scrapy/%E9%A1%B5%E9%9D%A2%E5%88%86%E6%9E%90/%E4%BF%A1%E4%BB%B6%E7%AE%A1%E7%90%86_%E8%AF%A6%E6%83%85.html'
    # 筛选IP正则表达式
    re_ip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')

    # 重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数
    def start_requests(self):
        """
        这是一个重载函数，它的作用是发出第一个Request请求
        :return:
        """
        # 带着headers、cookies去请求self.start_urls[0],返回的response会被送到
        # 回调函数parse中
        for url in self.start_urls:
            logging.info('admin url=' + url)
            # 因为我们上面定义了Rule，所以只需要简单的生成初始爬取Request即可
            # yield self.make_requests_from_url(url)
            yield Request(url, callback=self.parse_page)

    def parse_page(self, response):
        logging.info(response.url)
        title = response.xpath(
            '//div[@class="main-wrap"]/div[@class="path"]/p/a/text()').extract_first()
        if title is not None:
            logging.info(u'title：' + title)

        if title == '会员信件':
            messages = response.xpath('//*[@id="myform"]/table//tr')
            # ignore the table header row
            for message in messages[1:]:
                # 解析ID，拼接详情地址
                id = message.xpath('td[1]//text()').extract_first()
                url = self.message_url.format(id)
                yield Request(url, meta={'id': id}, callback=self.parse_message_page)
                break

            # 分页数据
            # page_pages = response.xpath('//*[@class="page_pages"]/text()').extract_first()
            # # 当前页码/总页码
            # pageNumber = page_pages.split('\/')[0]
            # totalPages = page_pages.split('\/')[1]
            # # 爬下一页数据
            # next_uri = 'http://www.8181.com.cn/admincp.php?c=message&ftype=&fkeyword=&ttype=&tkeyword=&sdate=&edate=&fromtype=&skeyword=&page=%s' % (
            #         int(pageNumber) + 1)
            # print(next_uri)
            # yield Request(next_uri, meta={'cookiejar': response.meta['cookiejar']}, callback=self.parse_page)

        if title == '会员列表':
            users = response.xpath('//*[@id="myform"]/table//tr')
            # ignore the table header row
            for user in users[1:]:
                # 解析ID，拼接详情地址
                id = user.xpath('td[1]//text()').extract_first()
                url = self.user_url.format(id)
                yield Request(url, meta={'id': id}, callback=self.parse_user_page)
                break

            # 分页数据
            # page_pages = response.xpath('//*[@class="page_pages"]/text()').extract_first()
            # page_pages = page_pages.strip()
            # # 当前页码/总页码
            # pageNumber = page_pages.split('/')[0]
            # totalPages = page_pages.split('/')[1]
            # next_uri = 'http://www.8181.com.cn/admincp.php?c=user&sgender=&sdist1=&sdist2=&sgroupid=&savatar=&slovesort=&smarry=&sdate=&edate=&sage=&eage=&sheight=&eheight=&sjobs=&ssalary=&esalary=&sedu=&eedu=&sflag=&selite=&sliehun=&sorderby=&srzemail=&srzmobile=&srzidnumber=&srzvideo=&srzqq=&showavatar=&srobot=&schild=&shouse=&scar=&shomedist1=&shomedist2=&fromtype=&searchtype=3&thintype=&thinid=0&page=1' % (
            #         int(pageNumber) + 1)
            # print(next_uri)
            # yield Request(next_uri, meta={'cookiejar': response.meta['cookiejar']}, callback=self.parse_page)

    def parse_user_page(self, response):
        '''
        解析会员详情页
        :param response:
        :return:
        '''
        id = response.meta['id']
        usertable = response.xpath('//*[@class="main-cont"]/table')
        # print(table)
        if usertable is not None:
            item = UserItem()
            item['id'] = usertable.xpath('//tr[1]/td[2]/text()').extract_first().strip()
            str = usertable.xpath('//tr[3]/td[2]').xpath('string(.)').extract_first()
            item['regip'] = ','.join(self.re_ip.findall(str))
            str = usertable.xpath('//tr[3]/td[4]').xpath('string(.)').extract_first()
            item['loginip'] = ','.join(self.re_ip.findall(str))
            yield item

    def parse_message_page(self, response):
        '''
        解析信件详情页
        :param response:
        :return:
        '''
        id = response.meta['id']
        msgtable = response.xpath('//*[@id="myform"]/table')
        if msgtable is not None:
            item = MessageItem()
            str = msgtable.xpath('//tr[1]/td[2]/text()').extract_first()
            item['id'] = str.split(' ')[0]
            item['content'] = msgtable.xpath('//tr[5]/td[2]/textarea/text()').extract_first()
            yield item
