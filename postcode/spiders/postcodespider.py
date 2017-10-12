# -*- coding: utf-8 -*-
import os
import urllib
import sys

from chardet import detect

from postcode.items import PostcodeItem

reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import re
import gzip
from scrapy import Selector, Request

class PostcodeSpider(scrapy.Spider):
    name = "postcodespider"
    host = "http://www.diqudaima.com"
    # 这个例子中只指定了一个页面作为爬取的起始url
    # 当然从数据库或者文件或者什么其他地方读取起始url也是可以的
    start_urls = [
        "http://www.diqudaima.com",
    ]
    # 爬虫的入口，可以在此进行一些初始化工作，比如从某个文件或者数据库读入起始url
    def start_requests(self):
        for url in self.start_urls:
            # 此处将起始url加入scrapy的待爬取队列，并指定解析函数
            # scrapy会自行调度，并访问该url然后把内容拿回来
            yield Request(url=url, callback=self.parse_homepage)

    # 版面解析函数，解析一个版面上的帖子的标题和地址
    def parse_homepage(self, response):
        selectorurl = Selector(response)
        province_list = selectorurl.xpath("//li")
        print len(province_list);
        print province_list[0]
        #exit(0)

        for i in range (0,len(province_list)-4):
            province_name = province_list[i].xpath("a/text()").extract()[0]
            province_url = province_list[i].xpath("a/@href").extract()[0]
            province_url = self.host + province_url
            print "province_name is : " + province_name
            print "province_url is : " + province_url
            item = PostcodeItem()
            item['province_name'] = province_name
            item['province_url'] = province_url
            yield Request(url=province_url, callback=self.parse_provincepage, meta={'item': item})
            #exit(0)

    def parse_provincepage(self, response):
        item = response.meta['item']
        selectorurl = Selector(response)
        city_list = selectorurl.xpath("//div[@class='all']/ul/li/a")
        for city in city_list:
            city_name = city.xpath("text()").extract()[0]
            city_url = city.xpath("@href").extract()[0]
            city_url = self.host + city_url
            # print "city_name is : " + city_name
            # print "city_url is : " + city_url
            item['city_name'] = city_name
            item['city_url'] = city_url

            yield Request(url=city_url, callback=self.parse_distpage, meta={'item': item})
            #exit(0)
        #exit(0)

    def parse_distpage(self, response):
        item = response.meta['item']
        selectorurl = Selector(response)
        city_name = selectorurl.xpath("//div[@class='title']/span/text()").extract()[2].split('>')[1]
        city_url = response.url
        print "city_name is : " + city_name
        print "city_url is : " + city_url
        #exit(0)
        dist_list = selectorurl.xpath("//div[@style='width:624px; float:left;']/ul/li")
        for dist in dist_list:
            dist_name = dist.xpath("a/text()").extract()[0]
            dist_url = dist.xpath("a/@href").extract()[0]
            dist_url = self.host + dist_url
            dist_content = dist.xpath("text()").extract()[0]
            # print "dist_name is : " + dist_name
            # print "dist_url is : " + dist_url
            distinctcode = dist_content.split(' ')[1]
            distinctcode = distinctcode.split('：')[1]
            postcode = dist_content.split(' ')[2]
            postcode = postcode.split('：')[1]
            areacode = dist_content.split(' ')[3]
            areacode = areacode.split('：')[1]
            #print "distinctcode is : " + distinctcode
            #print "postcode is : " + postcode
            #print "areacode is : " + areacode
            item['city_name'] = city_name
            item['city_url'] = city_url
            item['dist_name'] = dist_name
            item['dist_url'] = dist_url
            item['distinctcode'] = distinctcode
            item['postcode'] = postcode
            item['areacode'] = areacode

            print item['province_name']
            print item['province_url']
            print item['city_name']
            print item['city_url']
            print item['dist_name']
            print item['dist_url']
            print item['distinctcode']
            print item['postcode']
            print item['areacode']
            #exit(0)

            yield item
            #exit(0)




