from unittest import mock

import pytest

from jobsbrowser.items import PracujItem
from jobsbrowser.pipelines import JobsbrowserPipeline


@pytest.fixture()
def fake_item():
    return PracujItem(
        url='http://spam.egg',
        timestamp='2017-11-21 20:30:44.238471',
        raw_html='<b>Hello World!</b>',
        offer_id='5662378',
        date_posted='2017-09-31',
        valid_through='2017-09-31',
        employer='foobar it solutions',
        job_title='Spam Programmer',
        job_location='Warszawa, mazowieckie',
        job_description='<b>Hello World</b>',
    )


@pytest.fixture()
def jobsbrowser_pipeline():
    return JobsbrowserPipeline()


@pytest.fixture()
def spider():
    spider = mock.MagicMock()
    spider.settings = {'STORAGE_SERVICE_ADD_URL': 'foo.bar/add'}
    return spider


def test_jobsbrowser_pipeline_process_item_send_request_to_db_module(
    fake_item, jobsbrowser_pipeline, spider,
):
    with mock.patch('jobsbrowser.pipelines.requests.post') as post_mock:
        jobsbrowser_pipeline.process_item(fake_item, spider)
        post_mock.assert_called_once_with(
            spider.settings.get('STORAGE_SERVICE_ADD_URL'),
            data=dict(fake_item),
        )
