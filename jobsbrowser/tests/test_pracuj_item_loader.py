import pytest

from jobsbrowser.items import PracujItem
from jobsbrowser.loaders import (
    parse_date,
    PracujItemLoader,
)


@pytest.mark.parametrize('date_string', [
    '12,12,2017',
    '12$12$2017',
    '10.2017',
    '13/10/2017',
])
def test_parse_date_raise_value_error_for_unknown_format(date_string):
    with pytest.raises(ValueError):
        parse_date(date_string)


@pytest.mark.parametrize('date_string, expected', [
    ('12.12.2017', '2017-12-12'),
    ('2017-06-12', '2017-06-12'),
])
def test_parse_date_return_date_in_proper_format(date_string, expected):
        assert parse_date(date_string) == expected


class TestPracujItemLoader:
    @pytest.mark.parametrize('item_dict', [
        {
            'url': ['http://spam.egg'],
            'date_posted': ['2017-09-01'],
            'valid_through': ['2017-09-30'],
            'job_description': ['<b>Hello World</b>'],
        },
    ])
    def test_taking_first_from_each_field(self, item_dict):
        result = dict(self._pracuj_item_loader_from(**item_dict).load_item())
        assert all(not isinstance(field, list) for field in result.values())

    @pytest.mark.parametrize('url, expected', [
        (
            ['http://spam.egg/waw,programista-py,12345'],
            '12345',
        ),
        (
            ['http://spam.egg/,,,,,98765'],
            '98765',
        ),
    ])
    def test_offer_id_properly_extracted(self, url, expected):
        result = self._pracuj_item_loader_from(offer_id=url).load_item()
        assert result['offer_id'] == expected

    @pytest.mark.parametrize('item_dict, expected', [
        (
            {'employer': ['Spam'], 'job_title': ['Foo'], 'url': ['egg.com']},
            {'employer': 'Spam', 'job_title': 'Foo'}
        ),
        (
            {
                'employer': ['<div><spam>FC++</spam></div>'],
                'job_title': ['<b>CTO</b>'],
                'job_location': ['Łódź, mazowieckie'],
            },
            {'employer': 'FC++', 'job_title': 'CTO'}
        ),
    ])
    def test_remove_html_tags_from_employer_and_job_title_fields(
        self, item_dict, expected,
    ):
        result = self._pracuj_item_loader_from(**item_dict).load_item()
        assert {k: v for k, v in result.items() if k in expected} == expected

    @pytest.mark.parametrize('item_dict, expected', [
        (
            {'employer': ['Spam'], 'date_posted': ['22.10.2017']},
            {'employer': 'Spam', 'date_posted': '2017-10-22'}
        ),
        (
            {'valid_through': ['2014-11-20']},
            {'valid_through': '2014-11-20'}
        )
    ])
    def test_unify_date_in_date_posted_and_valid_through_fields(
        self, item_dict, expected,
    ):
        result = self._pracuj_item_loader_from(**item_dict).load_item()
        assert {k: v for k, v in result.items() if k in expected} == expected

    @staticmethod
    def _pracuj_item_loader_from(**kwargs):
        pracuj_item_loader = PracujItemLoader(item=PracujItem())
        for key, value in kwargs.items():
            pracuj_item_loader.add_value(key, value)
        return pracuj_item_loader
