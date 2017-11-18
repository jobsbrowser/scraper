import scrapy

from w3lib.html import remove_tags

from scrapy.loader import ItemLoader
from scrapy.loader.processors import (
    MapCompose,
    TakeFirst,
)


class PracujItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    offer_id_in = MapCompose(lambda value: value.rsplit(',', 1)[-1])
    employer_in = MapCompose(remove_tags)
    job_title_in = MapCompose(remove_tags)
