from datetime import datetime

import coloredlogs
import requests

from requests.exceptions import ConnectionError
from scrapy.http import Request
from scrapy.spiders import (
    CrawlSpider,
    Rule,
)
from scrapy.linkextractors import LinkExtractor

from jobsbrowser.items import PracujItem
from jobsbrowser.loaders import PracujItemLoader
from jobsbrowser.extractors import PracujLinkExtractor


class PracujSpider(CrawlSpider):
    name = 'pracuj'
    allowed_domains = ['pracuj.pl']
    start_urls = list()

    rules = (
        # following pagination
        Rule(LinkExtractor(restrict_css=(
            '.pager_item--next'
            '> a.pager_item_link'),
        )),
        # following job offers
        Rule(
            PracujLinkExtractor(
                restrict_css='#mainOfferList a[itemprop="title"]',
                filter_link='filter_link',
            ),
            callback='parse_item',
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._already_parsed_links = None
        # compile PracujLinkExtractors
        for rule in self._rules:
            if (isinstance(rule.link_extractor, PracujLinkExtractor) and
                    not callable(rule.link_extractor.filter_link)):
                rule.link_extractor.filter_link = getattr(
                    self,
                    rule.link_extractor.filter_link or '',
                    lambda *args: True,  # accept all links
                )

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

    def start_requests(self):
        """Create start_urls and yield requests to them.

        Add `category_name` to `request.meta` dictionary.
        `category_name` is passed down in `_requests_to_follow`
        method to each new request.
        """

        url_template = 'http://pracuj.pl/praca?cc={category_id}'
        offers_last_days = self.settings.get('PRACUJ_OFFERS_FROM_LAST_N_DAYS')
        if offers_last_days:
            url = f'{url_template}&p={offers_last_days}'
        for category_id, name in self.settings['PRACUJ_CATEGORIES'].items():
            url = url_template.format(category_id=category_id)
            self.start_urls.append(url)
            yield Request(
                url,
                dont_filter=True,
                meta={'category_name': name},
            )

    def filter_link(self, link, category_name):
        """Filter pracuj.pl offer link.

        Update all already filtered links category name.
        """
        result = link in self.already_parsed_links
        if result:
            self.logger.debug(f'Updating categories of offer: {link}.')
            try:
                requests.put(
                    self.settings['STORAGE_SERVICE_UPDATE_URL'],
                    json={'url': link, 'category_name': category_name},
                )
            except ConnectionError:
                self.logger.warning(
                    "Couldn't connect to storage service to update offer."
                )
        return not result

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
        pracuj_item.add_value(
            'categories',
            response.meta['category_name'],
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

    def _requests_to_follow(self, response):
        for request in super()._requests_to_follow(response):
            request.meta.setdefault(
                'category_name',
                response.meta['category_name'],
            )
            yield request
