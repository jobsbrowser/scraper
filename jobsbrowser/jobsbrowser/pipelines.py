# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.utils.serialize import ScrapyJSONEncoder

from .tasks import send_offer


class JobsbrowserPipeline(object):
    def process_item(self, item, spider):
        spider.logger.info(f"Sending item {item['offer_id']} to queue")
        send_offer.delay(dict(item))
