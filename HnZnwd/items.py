# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HnznwdItem(scrapy.Item):
    # define the fields for your item here like:
    q = scrapy.Field()
    a = scrapy.Field()
