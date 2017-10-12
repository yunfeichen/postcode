# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostcodeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    province_name = scrapy.Field()
    province_url = scrapy.Field()
    city_name = scrapy.Field()
    city_url = scrapy.Field()
    dist_name = scrapy.Field()
    dist_url = scrapy.Field()
    distinctcode = scrapy.Field()
    postcode = scrapy.Field()
    areacode = scrapy.Field()
    pass
