import contextlib

from unittest import mock

from scrapy import signals
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from jobsbrowser.spiders.pracuj import PracujSpider


@contextlib.contextmanager
def temporary_attribute_change(obj, **kwargs):
    old_attrs = dict()
    for attr_name, new_value in kwargs.items():
        if hasattr(obj, attr_name):
            old_attrs[attr_name] = getattr(obj, attr_name)
            setattr(obj, attr_name, new_value)
    yield obj
    for attr_name, old_value in old_attrs.items():
        setattr(obj, attr_name, old_value)


class TestPracujSpider:
    def test_get_already_parsed_links_send_request_to_db_module(self):
        with mock.patch('jobsbrowser.spiders.pracuj.requests.get') as get_mock:
            spider = PracujSpider()
            spider.settings = get_project_settings()
            links = spider.already_parsed_links
            get_mock.assert_called_once_with(
                spider.settings['STORAGE_SERVICE_RETRIEVE_URL'],
            )
            assert links == spider.already_parsed_links
            assert get_mock.call_count == 1

    def test_spider_raise_error_when_invalid_url(self):
        with temporary_attribute_change(
            PracujSpider,
            allowed_domains=['spam.egg'],
            start_urls=['http://spam.egg/beacon'],
            start_requests=lambda self: [
                Request(self.start_urls[0], dont_filter=True),
            ],
        ) as spider_class_with_invalid_url:
            crawler, *_ = self._start_crawling(spider_class_with_invalid_url)
            stats = crawler.stats
            dns_lookup_error_count = stats.get_value(
                ('downloader/exception_type_count/twisted.internet.error.'
                 'DNSLookupError'),
                0,
            )
            assert dns_lookup_error_count > 0

    @staticmethod
    def _start_crawling(
        spider_class=PracujSpider, collect_items=True, **kwargs
    ):
        settings = get_project_settings()
        settings.update(kwargs)
        crawler_process = CrawlerProcess(settings)
        spider = spider_class()
        crawler_process.crawl(spider)
        crawler = list(crawler_process.crawlers)[0]
        storage = list()
        if collect_items:
            crawler.signals.connect(
                lambda item: storage.append(item),
                signals.item_scraped,
            )
        crawler_process.start()
        return crawler, spider, storage
