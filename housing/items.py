# -*- coding: utf-8 -*-

import scrapy


class HousingItem(scrapy.Item):

    date_posted = scrapy.Field()
    description = scrapy.Field()
    location = scrapy.Field()
    rent = scrapy.Field()
    season = scrapy.Field()
    availability = scrapy.Field()
    details = scrapy.Field()
    contact = scrapy.Field()
