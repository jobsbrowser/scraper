import pytest

from jobsbrowser.items import PracujItem
from jobsbrowser.loaders import PracujItemLoader


class TestPracujItemLoader:
    @pytest.mark.parametrize('item_dict', [
        {
            'url': ['http://spam.egg'],
            'date_posted': ['2017-09-31'],
            'valid_through': ['2017-09-31'],
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

    @staticmethod
    def _pracuj_item_loader_from(**kwargs):
        pracuj_item_loader = PracujItemLoader(item=PracujItem())
        for key, value in kwargs.items():
            pracuj_item_loader.add_value(key, value)
        return pracuj_item_loader
