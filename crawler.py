from html.parser import HTMLParser
import threading


class Crawler:
    def __init__(self, url, getter):
        self.links_to_visit = [url]
        self.visited_links = []
        self.get = getter

    def start(self, iterations):
        links_discovered = []
        for link in self.links_to_visit:
            response = self.get(link)
            links = extract_links(response.content, link)
            links_discovered.extend(links)
            self.visited_links.append(link)

        self.links_to_visit = links_discovered

        if iterations > 0:
            thread = threading.Thread(target=self.start, args=iterations -1)
            thread.start()


class LinkParser(HTMLParser):
    def __init__(self, base_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url
        self.link_hrefs = set()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    if "http" not in value:
                        value = self.base_url + value
                    self.link_hrefs.add(value)


def extract_links(text, base_url):
    parser = LinkParser(base_url)
    parser.feed(str(text, "utf8"))
    return list(parser.link_hrefs)
