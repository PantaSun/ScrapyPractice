# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from scrapy.pipelines.images import ImagesPipeline
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open("article.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MysqlPipeline(object):
    """同步插入数据库"""
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '', 'article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into article(title, url, create_date, fav_nums, url_object_id)
            VALUES (%s, %s, %s, %s)
        
        """
        self.cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['fav_nums'],
                                         item['url_object_id']))
        self.conn.commit()
        return item


class MysqlTwistedPipeline(object):
    """异步插入数据库"""
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls,settings):
        db_parms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        db_pool = adbapi.ConnectionPool('MySQLdb', **db_parms)
        return cls(db_pool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.db_pool.runInteraction(self.do_insert, item)
        query.addErrback(self.hand_error)
        return item

    def do_insert(self, cursor, item):
        insert_sql = """
            insert into article(title, url, create_date, fav_nums, url_object_id, praise_nums, comment_nums, 
            front_img_url, content, tags)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

        """

        cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['fav_nums'],
                                    item['url_object_id'], item['praise_nums'], item['comment_nums'],
                                    item['front_img_url'][0], item['content'], item['tags']
                                    ))

    def hand_error(self, failure):
        # 处理异步插入的异常
        print(failure)


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if 'front_img_url' in item:
            for ok, value in results:
                front_img_path = value['path']

            item['front_img_path'] = front_img_path
        return item


