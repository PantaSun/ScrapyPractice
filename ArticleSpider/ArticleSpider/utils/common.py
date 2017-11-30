#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/27 15:43
# @Author  : Panta Sun
# @Site    : 
# @File    : common.py
# @Software: PyCharm
import hashlib


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

#
# if __name__ == "__main__":
#     print(get_md5("http://www.baidu.com"))