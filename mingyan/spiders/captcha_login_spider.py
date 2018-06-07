#!/usr/bin/env python
# -*- coding:utf-8 -*
import scrapy
from scrapy import Request, FormRequest
import json
from PIL import Image
from io import BytesIO
import pytesseract
from scrapy.log import logger

class CaptchaLoginSpider(scrapy.Spider):
    name = "login_captcha"
    start_urls = ['http://member.yunwangke.com/']

    def parse(self, response):
        pass

    login_url = 'http://lmcms.leimingtech.com/lmcms'
    username = 'admin'
    password = '123456'

    def start_requests(self):
        yield Request(self.login_url, callback=self.login)

    def login(self, response):
        login_response = response.meta.get('login_response')
        if not login_response:
            captchaUrl = response.css('#randCodeImage::attr(src)').extract_first()

            captchaUrl = response.urljoin(captchaUrl)
            print("验证码URL:" + captchaUrl)
            # scrapy默认会过滤重复网页，发起Request添加dont_filter = True，则可以重复请求
            yield Request(captchaUrl, callback=self.login, meta={'login_response': response}, dont_filter=True)

        else:

            formdata = {'userName': self.username, 'password': self.password,
                        'randCode': self.get_captcha_by_OCR(response.body)}
            url = 'http://lmcms.leimingtech.com/lmcms/loginAction.do?checkuser'
            yield FormRequest(url=url,callback=self.parse_login,
                                            formdata=formdata,dont_filter=True)

    def parse_login(self, response):
        #巨坑!! 搞了两个小时,因为json外侧不能有" 号...
        response_text = response.text.replace("\"{","{").replace("}\"","}").replace("\\","")
        result = json.loads(response_text)
        print(response_text)
        print("登录结果:"+str(result['isSuccess']))
        if result['isSuccess']:
            logger.info('登录成功')
            return super().start_requests()
        logger.info("登录失败,重新登录。")
        return self.start_requests()

    def get_captcha_by_OCR(self, data):
        img = Image.open(BytesIO(data))
        img = img.convert('L')
        # img.show()
        captcha = pytesseract.image_to_string(img)
        print("captcha:" + captcha)
        img.close()
        return captcha
