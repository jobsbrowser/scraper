from datetime import datetime

from scrapy.loader import ItemLoader
from scrapy.loader.processors import (
    MapCompose,
    TakeFirst,
)
from scrapy.utils.project import get_project_settings
from w3lib.html import remove_tags


def parse_date(date_string):
    """Parse date and return it in new format.

    Parses input date using formats from settings.INPUT_DATE_FORMATS.
    Raises ValueError for unparsable input date.
    Returns date in format from settings.OUTPUT_DATE_FORMAT.
    """
    settings = get_project_settings()
    date_formats = settings.get('INPUT_DATE_FORMATS')
    target_format = settings.get('OUTPUT_DATE_FORMAT')
    date = None
    for date_format in date_formats:
        try:
            date = datetime.strptime(date_string, date_format)
        except ValueError:
            continue
        else:
            return datetime.strftime(date, target_format)
    raise ValueError('Invalid date format')


class PracujItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    offer_id_in = MapCompose(lambda value: value.rsplit(',', 1)[-1])
    employer_in = MapCompose(remove_tags)
    job_title_in = MapCompose(remove_tags)
    valid_through_in = MapCompose(parse_date)
    date_posted_in = MapCompose(parse_date)
    categories_out = MapCompose(lambda x: [x])
