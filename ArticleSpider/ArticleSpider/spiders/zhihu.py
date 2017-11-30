# -*- coding: utf-8 -*-
import scrapy
import re

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
    }

    def parse(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request("https://www.zhihu.com/#signin", headers=self.headers, callback=self.login)]

    def login(self, response):
        text = response.text
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', text, re.DOTALL)
        xrsf = ''
        if match_obj:
            xrsf = (match_obj.group(1))
        if xrsf:
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xrsf": xrsf,
                "password": "s7703835",
                "phone_num": "15529260661",
                "captcha_type": "cn"}
            return [scrapy.FormRequest(
                url=post_url,
                formdata=post_data,
                headers=self.headers,
                callback=self.check_login
            )]

    def check_login(self, response):
        """
        验证登录是否成功
        :param response:
        :return:
        """
        pass
