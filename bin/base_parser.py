import re

import requests

from bin.url_builder import UrlBuilder


class BaseParser:
    href_url_regex = re.compile(r'href="(?P<url>[^"]*)"')
    url_filter_regex = re.compile(r'^https?://([^/\s\'"]*/?)*$')

    def __init__(self, url):
        self.url = url
        if type(self.url_filter_regex) == str:
            self.url_filter_regex = re.compile(self.url_filter_regex)

    # main function. returns new_urls. any data is the responsibility of subclasses
    def parse(self):
        # get text
        text = self.load_page()

        # subclass does their stuff
        self.parse_page(text)

        # get new urls, and filter. return those to worker
        new_urls = list(filter(lambda x: self.url_filter_regex.match(x), self.parse_all_urls(text)))
        return new_urls

    # get html code from url
    def load_page(self):
        # TODO try catch. retry policy.
        print('Loading "%s"..."' % self.url)
        page = requests.get(self.url)
        print('"%s" loaded!' % self.url)
        return page.text

    # get urls from text
    # TODO generalize
    def parse_all_urls(self, text):
        matches = self.href_url_regex.findall(text)
        new_urls = [UrlBuilder.build_qualified(self.url, match) for match in matches]
        return new_urls

    # parse page for content
    def parse_page(self, text):
        pass
