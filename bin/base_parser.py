import re
import threading

import requests
import time

from bin.url_builder import UrlBuilder


class BaseParser:
    number_retries = 5
    timeout = 5
    href_url_regex = re.compile(r'href="(?P<url>[^"]*)"')
    url_filter_regex = re.compile(r'^https?://[^\s]+$')

    def __init__(self, url):
        self.url = url
        if type(self.url_filter_regex) == str:
            self.url_filter_regex = re.compile(self.url_filter_regex)

    # main function. returns new_urls. any data is the responsibility of subclasses
    def parse(self):
        print('Parsing %s' % self.url)

        # get text
        try:
            text = self.load_page()
        except requests.exceptions.RequestException as e:
            print('Error loading "%s". Error is %s' % (self.url, e))
            return ['']  # no new urls

        # subclass does their stuff
        self.parse_page(text)

        # get new urls, and filter. return those to worker
        all_urls = self.parse_all_urls(text)
        new_urls = list(filter(lambda x: self.url_filter_regex.match(x), all_urls))
        return new_urls

    # get html code from url
    def load_page(self):
        attempts = 0
        while True:
            try:
                page = requests.get(self.url, timeout=self.timeout)
                break

            except requests.exceptions.Timeout as e:
                attempts += 1
                if attempts == self.number_retries:
                    raise requests.exceptions.RequestException() from e

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
