import pytest
import requests

import crawler


@pytest.fixture
def getter():
    def mock_get(url):

        def internet_forever():
            counter = 1
            while True:
                response = requests.Response()
                page = f'<html><a href="https://www{counter}.touchsurgery.com"></a></html>'
                response._content = bytes(page, 'utf8')
                counter += 1
                yield response

        if not hasattr(mock_get, 'generator'):
            mock_get.generator = internet_forever()

        return next(mock_get.generator)

    return mock_get


def test_crawler_visits_site_and_discovers_links(getter):
    spider = crawler.Crawler('https://www.example.com', getter)

    spider.start(iterations=0)

    assert spider.links_to_visit == ['https://www1.touchsurgery.com']


def test_crawler_recurses_into_discovered_links(getter):
    spider = crawler.Crawler('https://www.example.com', getter)

    spider.start(iterations=2)

    assert spider.visited_links == [
        'https://www.example.com',
        'https://www1.touchsurgery.com',
        'https://www2.touchsurgery.com'
    ]
