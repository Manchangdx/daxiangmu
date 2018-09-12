# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class JobItem(scrapy.Item):
    title = scrapy.Field()
    city = scrapy.Field()
    salary = scrapy.Field()
    exp_edu = scrapy.Field()
    #education = scrapy.Field()
    tags = scrapy.Field()
    company = scrapy.Field()
