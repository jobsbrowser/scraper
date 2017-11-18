# -*- coding: utf-8 -*-
from datetime import datetime

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
        ),
    )

    def parse_item(self, response):
        self.logger.info('STARTING parsing item')
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
        pracuj_item.add_value(
            'raw_html',
            response.body_as_unicode(),
        )
        pracuj_item.add_value(
            'offer_id',
            response.url,
        )
        pracuj_item.add_css(
            'date_posted',
            'span[itemprop="datePosted"]',
            re=date_regexp,
        )
        pracuj_item.add_css(
            'valid_through',
            'span[itemprop="validThrough"]',
            re=date_regexp,
        )
        pracuj_item.add_css(
            'employer',
            'h2[itemprop="hiringOrganization"]',
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
            '#description',
        )
        return pracuj_item.load_item()
