from bin import BaseConcurrentParser
from bin.base_parser import BaseParser
from bin.router import Route

ROOT = 'https://en.wikipedia.org/wiki/Main_Page'


@Route(r'^https?://en.wikipedia.org/wiki/([^/\s\'"]*/?)*$')
class WikipediaParser(BaseParser):
    url_filter_regex = r'^https?://en.wikipedia.org/wiki/([^/\s\'"]*/?)*$'

    def parse_page(self, text):
        # TODO parse logic goes here
        print('You\'re at %s. HTML is in page. do your\'re stuff' % self.url)


def run():
    pool = BaseConcurrentParser(ROOT, 10, 50)
    pool.start()
    pool.join()
    print('Done!')
