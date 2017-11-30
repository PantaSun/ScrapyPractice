# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader
import datetime
import re

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItemLoader(ItemLoader):
    """自定义itemloader"""
    default_output_processor = TakeFirst()


def add_jobbole(value):
    return value + "--Jobbole"


def date_convert(create_date):
    try:
        create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d")
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def get_nums(value):
    match_re = re.match(".*?(\d+).*?", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def return_value(value):
    return value


class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(add_jobbole))
    create_date = scrapy.Field(input_processor=MapCompose(date_convert))
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_img_url = scrapy.Field(output_processor=MapCompose(return_value))
    front_img_path = scrapy.Field()
    praise_nums = scrapy.Field(input_processor=MapCompose(get_nums))
    comment_nums = scrapy.Field(input_processor=MapCompose(get_nums))
    fav_nums = scrapy.Field(input_processor=MapCompose(get_nums))
    tags = scrapy.Field(output_processor=Join())
    # tags = scrapy.Field()
    content = scrapy.Field()
