# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import datetime

dbuser = 'root'
dbpass = ''
dbname = 'postcode'
dbhost = '127.0.0.1'
dbport = '3306'

class PostcodePipeline(object):
    def process_item(self, item, spider):
        return item

class MySQLStorePipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user=dbuser, passwd=dbpass, db=dbname, host=dbhost, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()
        # 清空表：
        # self.cursor.execute("truncate table weather;")
        self.conn.commit()

    def process_item(self, item, spider):
        curTime = datetime.datetime.now()
        try:
            self.cursor.execute("""INSERT INTO postcode (province_name, province_url, city_name, city_url, dist_name, dist_url , distinctcode, postcode, areacode, updateTime)  
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                (
                                    item['province_name'].encode('utf-8'),
                                    item['province_url'].encode('utf-8'),
                                    item['city_name'].encode('utf-8'),
                                    item['city_url'].encode('utf-8'),
                                    item['dist_name'].encode('utf-8'),
                                    item['dist_url'].encode('utf-8'),
                                    item['distinctcode'].encode('utf-8'),
                                    item['postcode'].encode('utf-8'),
                                    item['areacode'].encode('utf-8'),
                                    curTime,
                                )
                                )

            self.conn.commit()


        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return item