import threading

from bin.base_parser import BaseParser
from bin.router import RouteManager


class BaseWorker(threading.Thread):
    parse_class = BaseParser

    def __init__(self, tid, context):
        super().__init__()
        self.tid = tid
        self.context = context

    def run(self):
        print('Hello from thread %s!' % self.tid)

        while True:
            # get new url
            new_url = self.context.pubsub.pop()

            # parse
            # im not sure if i should feel ashamed or proud
            # its probably ashamed :(
            # ...
            # parser_cls = RouteManager.route(new_url)
            # new_urls = parser_cls(new_url).parse()
            new_urls = RouteManager.route(new_url)(new_url).parse()

            # add new urls to master urls queue
            self.context.pubsub.push_group(new_urls)

            # check exit condition
            if self.context.pubsub.popped >= self.context.page_limit:
                return

        print('%s: Done!' % self.tid)
