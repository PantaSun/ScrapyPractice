#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/30 20:43
# @Author  : Panta Sun
# @Site    : 
# @File    : zhihu_login_requests.py
# @Software: PyCharm
import requests
import re

try:
    import cookielib
except Exception as e:
    import http.cookiejar as cookielib

session =requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies")
try:
    session.cookies.load(ignore_discard=True)
except Exception as e:
    print("cookie未能加载")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
}

login_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Length": "96",
    "Origin": "https://www.zhihu.com",
    "X-Xsrftoken": ""
}


def get_xrsf():
    """获取_xsrf"""
    response = requests.get("https://www.zhihu.com", headers=headers)
    # text = '<input type="hidden" name="_xsrf" value="a5b60f904c5e11a7e41d8934f401f223"/>'
    match_obj = re.findall('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return match_obj[0]


def get_index():
    response = session.get("https://www.zhihu.com", headers=headers)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))


def zhihu_login(account, password):
    """登录知乎"""
    _xrsf = get_xrsf()
    if re.match("^1\d{10}", account):
        print("手机账号登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xrsf": _xrsf,
            "password": password,
            "phone_num": account,
            "captcha_type": 'cn'
        }
        my_login_headers = login_headers
        my_login_headers["X-Xsrftoken"] = _xrsf
        response_text = requests.post(post_url, data=post_data, headers=my_login_headers)

        session.cookies.save()
    else:
        print("邮箱账号登录")
        post_url = "https://www.zhihu.com/login/email"
        post_data = {
            "_xrsf": get_xrsf(),
            "password": password,
            "email": account,
            "captcha_type": 'cn'
        }

        response_text = session.post(post_url, data=post_data, headers=headers)

        session.cookies.save()


zhihu_login("15529260661", "s7703835")
# get_index()
