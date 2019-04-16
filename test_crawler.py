import pytest
import requests

import crawler


@pytest.fixture
def getter(request):
    def mock_get(url):
        def internet_forever():
            counter = 1
            while True:
                if "relative_url" in str(request.function):
                    host = ""
                else:
                    host = "https://www.touchsurgery.com"
                response = requests.Response()
                page = f'<html><a href="{host}/{counter}"></a></html>'
                response._content = bytes(page, "utf8")
                counter += 1
                yield response

        if not hasattr(mock_get, "generator"):
            mock_get.generator = internet_forever()

        return next(mock_get.generator)

    return mock_get


def test_crawler_visits_site_and_discovers_links(getter):
    spider = crawler.Crawler("https://www.example.com", getter)

    spider.start(iterations=0)

    assert spider.links_to_visit == ["https://www.touchsurgery.com/1"]


def test_crawler_recurses_into_discovered_links(getter):
    spider = crawler.Crawler("https://www.example.com", getter)

    spider.start(iterations=2)

    assert spider.visited_links == [
        "https://www.example.com",
        "https://www.touchsurgery.com/1",
        "https://www.touchsurgery.com/2",
    ]


def test_crawler_handles_discovering_relative_urls(getter, request):
    spider = crawler.Crawler("https://www.example.com", getter)

    spider.start(iterations=2)

    assert spider.visited_links == [
        "https://www.example.com",
        "https://www.example.com/1",
        "https://www.example.com/1/2",
    ]
