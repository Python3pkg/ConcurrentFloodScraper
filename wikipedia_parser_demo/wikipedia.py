from bin import BaseConcurrentParser
from bin.base_parser import BaseParser
from bin.router import Route

ROOT = 'https://en.wikipedia.org/wiki/Main_Page'


@Route(r'^https?://en.wikipedia.org/wiki/([^/\s\'"]*/?)*$')
class WikipediaParser(BaseParser):
    url_filter_regex = r'^https?://en.wikipedia.org/wiki/([^/\s\'"]*/?)*$'

    def parse_page(self, text):
        # TODO parse logic goes here
        print('routing works')


def run():
    pool = BaseConcurrentParser(ROOT, 5, 20)
    pool.start()
    pool.join()
    print('Done!')
