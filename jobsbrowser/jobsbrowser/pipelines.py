# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests

from requests.exceptions import ConnectionError


class JobsbrowserPipeline(object):
    def process_item(self, item, spider):
        offer_id = item['offer_id']
        spider.logger.info(
            f"Offer {offer_id} scraped. Sending to storage service...")
        try:
            r = requests.post(
                spider.settings["STORAGE_SERVICE_ADD_URL"], json=dict(item)
            )
        except ConnectionError:
            spider.logger.warning(
                f"Sending offer {offer_id} failed. "
                "Service storage is unavailable."
            )
        else:
            spider.logger.info(
                f"Offer {offer_id} sent to storage service. "
                f"Returned Code: {r.status_code}"
            )
        return item
