#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/30 20:43
# @Author  : Panta Sun
# @Site    : 
# @File    : zhihu_login_requests.py
# @Software: PyCharm
import requests
import re
import time
from PIL import Image
import os.path

try:
    import cookielib
except Exception as e:
    import http.cookiejar as cookielib

session =requests.Session()
session.cookies = cookielib.LWPCookieJar(filename="cookies")
try:
    session.cookies.load(ignore_discard=True)
except Exception as e:
    print("cookie未能加载")

headers = {
    #"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
}


def get_xsrf():
    """获取_xsrf"""
    response = session.get("https://www.zhihu.com", headers=headers)
    # text = '<input type="hidden" name="_xsrf" value="a5b60f904c5e11a7e41d8934f401f223"/>'
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text, re.DOTALL)
    if match_obj:
        return match_obj.group(1)


def get_index():
    response = session.get("https://www.zhihu.com", headers=headers)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))


def is_login():
    pass


def get_verification_code():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha


def zhihu_login(account, password):
    """登录知乎"""
    _xsrf = get_xsrf()
    headers["X-Xsrftoken"] = _xsrf
    headers["X-Requested-With"] = "XMLHttpRequest"
    if re.match("^1\d{10}", account):
        print("手机账号登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xrsf": _xsrf,
            "password": password,
            "phone_num": account,
            "captcha_type": 'cn'
        }
    elif "@" in account:
        print("邮箱账号登录")
        post_url = "https://www.zhihu.com/login/email"
        post_data = {
            "_xrsf": _xsrf,
            "password": password,
            "email": account,
            "captcha_type": 'cn'
        }
    response = requests.post(post_url, data=post_data, headers=headers)
    if response.json()["r"] == 1:
        print("需要验证码")
        post_data["captcha"] = get_verification_code()
        response = session.post(post_url, data=post_data, headers=headers)
        response_code = response.json()
        print(response_code['msg'])
     # 保存 cookies 到文件，
     # 下次可以使用 cookie 直接登录，不需要输入账号和密码
    session.cookies.save()


zhihu_login("15529260661", "s7703835")
# get_index()
# print(get_xrsf())