# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Showing(scrapy.Item):
    listing_id = scrapy.Field()
    price = scrapy.Field()
    address = scrapy.Field()
    unit_no = scrapy.Field()
    city = scrapy.Field()
    listing_url = scrapy.Field()
    start_tm = scrapy.Field()
    end_tm = scrapy.Field()
    agent_name = scrapy.Field()
    agent_email = scrapy.Field()
    agent_phone = scrapy.Field()
    broker_name = scrapy.Field()
