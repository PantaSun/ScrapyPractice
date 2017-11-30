# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse
from scrapy.http import Request
from scrapy.loader import ItemLoader
from ArticleSpider.items import JobboleArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5
import datetime


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. 解析列表页中所有文章的url并交给scrapy下载后进行解析
        2. 提取下一页的url并提交给scrapy进行下载，下载后交给parse
        :param response:
        :return:
        """
        # 解析列表页中所有文章的url并交给scrapy下载后进行解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css('img::attr(src)').extract_first("")
            post_url = post_node.css('::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"font_img_url": image_url}, callback=self.parse_detail)

        # 提取下一页的url并提交给scrapy进行下载，下载后交给parse
        next_url = response.css('.next.page-numbers::attr(href)').extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        """通过css选择器提取页面内容"""
        article_item = JobboleArticleItem()
        # title = response.css(".entry-header h1::text").extract()[0]
        # front_img_url = response.meta.get("font_img_url", "")
        # create_date = response.css(".entry-meta p::text").extract()[0].replace("·", "").strip()
        # praise_nums = response.css(".post-adds span h10::text").extract()[0]
        # fav_nums = response.css(".bookmark-btn::text").extract()[0].strip()
        # match_re = re.match(".*?(\d+).*?", fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        # comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        # match_re = re.match(".*?(\d+).*?", comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        # content = response.css(".entry").extract()[0]
        # tag_list = response.css(".entry-meta a::text").extract()
        # tags = ','.join(tag_list)
        # try:
        #     create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d")
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()

        # article_item['title'] = title
        # article_item['url'] = response.url
        # article_item['url_object_id'] = get_md5(response.url)
        # article_item['front_img_url'] = [front_img_url]
        # article_item['create_date'] = create_date
        # article_item['praise_nums'] = praise_nums
        # article_item['fav_nums'] = fav_nums
        # article_item['comment_nums'] = comment_nums
        # article_item['content'] = content
        # article_item['tags'] = tags

        # 通过 itemloader 加载item
        front_img_url = response.meta.get("font_img_url", "")
        item_loader = ArticleItemLoader(item=JobboleArticleItem(), response=response)
        # item_loader = ItemLoader(item=JobboleArticleItem(), response=response)
        item_loader.add_css('title', '.entry-header h1::text')
        item_loader.add_css('create_date', '.entry-meta p::text')
        item_loader.add_css('praise_nums', '.post-adds span h10::text')
        item_loader.add_css('fav_nums', '.bookmark-btn::text')
        item_loader.add_css('comment_nums', 'a[href="#article-comment"] span::text')
        item_loader.add_css('tags', '.entry-meta p a::text')
        item_loader.add_css('content', '.entry')
        # item_loader.add_xpath()
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_value('front_img_url', [front_img_url])
        article_item = item_loader.load_item()

        yield article_item
