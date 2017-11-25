# -*- coding: utf-8 -*-
from datetime import datetime

import coloredlogs
import requests
from requests.exceptions import ConnectionError
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import (
    CrawlSpider,
    Rule,
)

from jobsbrowser.items import PracujItem
from jobsbrowser.loaders import PracujItemLoader


class PracujSpider(CrawlSpider):
    name = 'pracuj'
    allowed_domains = ['pracuj.pl']
    start_urls = ['http://pracuj.pl/praca?cc=5013%2c5015%2c5016']

    rules = (
        # following pagination
        Rule(LinkExtractor(restrict_css=(
            '.desktopPagin_item:last-child:not(.current)'
            '> a.desktopPagin_item_link'),
        )),
        # following job offers
        Rule(
            LinkExtractor(
                restrict_css='#mainOfferList a[itemprop="title"]',
            ),
            callback='parse_item',
            process_links='filter_links',
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._already_parsed_links = None

    @property
    def logger(self):
        logger = super().logger
        coloredlogs.install(
            level=self.settings['LOG_LEVEL'], logger=logger.logger)
        return logger

    @property
    def already_parsed_links(self):
        if self._already_parsed_links is None:
            self._already_parsed_links = self._get_already_parsed_links()
        return self._already_parsed_links

    def filter_links(self, links):
        self.logger.debug(f"Before filter: {len(links)} links")
        result = [link for link in links
                  if link.url not in self.already_parsed_links]
        self.logger.debug(f"After filter: {len(result)} links")
        return result

    def parse_item(self, response):
        self.logger.debug(f"Parsing item: {response.url}")
        date_regexp = r'\d+.\d+.\d+'
        location_regexp = r'.+,\s*[\w-]+'
        pracuj_item = PracujItemLoader(item=PracujItem(), response=response)
        pracuj_item.add_value(
            'url',
            response.url,
        )
        pracuj_item.add_value(
            'timestamp',
            str(datetime.utcnow()),
        )
        pracuj_item.add_css(
            'raw_html',
            '#offer',
        )
        pracuj_item.add_value(
            'offer_id',
            response.url,
        )
        pracuj_item.add_css(
            'date_posted',
            '[itemprop="datePosted"]',
            re=date_regexp,
        )
        pracuj_item.add_css(
            'valid_through',
            '[itemprop="validThrough"]',
            re=date_regexp,
        )
        pracuj_item.add_css(
            'employer',
            '[itemprop="hiringOrganization"]',
        )
        pracuj_item.add_css(
            'job_title',
            '#offerTitle',
        )
        pracuj_item.add_css(
            'job_location',
            '[itemprop="addressRegion"]',
            re=location_regexp,
        )
        pracuj_item.add_css(
            'job_description',
            '[itemprop="description"]',
        )
        pracuj_item.add_css(
            'job_benefits',
            '[itemprop="benefits"]',
        )
        pracuj_item.add_css(
            'job_qualifications',
            '[itemprop="qualifications"]',
        )
        return pracuj_item.load_item()

    def _get_already_parsed_links(self):
        links = set()
        try:
            response = requests.get(
                self.settings['STORAGE_SERVICE_RETRIEVE_URL']
            )
            links = set(response.json()["links"])
        except ConnectionError:
            self.logger.warning(
                "Couldn't connect to storage service to retrieve "
                "parsed offers. All available offers will be parsed."
            )
        except (KeyError, TypeError, ValueError):
            self.logger.warning(
                "Storage service returned response that can't be used. "
                "All available offers will be parsed."
            )
        finally:
            return links
