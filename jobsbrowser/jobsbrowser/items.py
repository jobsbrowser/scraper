# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class JobsbrowserItem(scrapy.Item):
    url = scrapy.Field()
    timestamp = scrapy.Field()
    raw_html = scrapy.Field()


class PracujItem(JobsbrowserItem):
    offer_id = scrapy.Field()
    date_posted = scrapy.Field()
    valid_through = scrapy.Field()
    employer = scrapy.Field()
    job_title = scrapy.Field()
    job_location = scrapy.Field()
    job_description = scrapy.Field()
    job_benefits = scrapy.Field()
    job_qualifications = scrapy.Field()
