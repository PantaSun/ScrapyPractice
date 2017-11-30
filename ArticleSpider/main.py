#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/23 16:01
# @Author  : Panta Sun
# @Site    : 
# @File    : main.py
# @Software: PyCharm
from scrapy.cmdline import execute
import os
import sys

print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(['scrapy', 'crawl', 'jobbole'])
execute(['scrapy', 'crawl', 'zhihu'])