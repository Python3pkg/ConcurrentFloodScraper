from bin.base_worker import BaseWorker
from bin.pubsub import PubSub, SetQueue

from bin.ticker import Ticker


# global context for threads
class Context:
    # pubsub is dependency injected
    def __init__(self, pubsub):
        self.pages_parsed = 0
        self.page_limit = 0  # get overriden, declared here for verbosity
        self.pubsub = pubsub


# baseline controller class, controls worker threads
class BaseController:
    worker_class = BaseWorker
    pubsub_class = PubSub
    queue_class = SetQueue

    def __init__(self, num_workers):
        queue = self.queue_class()
        pubsub = self.pubsub_class(queue)
        self.context = Context(pubsub)
        self.workers = [self.get_new_worker(i) for i in range(num_workers)]
        self.ticker = Ticker(self.context)

    # returns a new worker. This allows Controller child classes an easy way to take over worker construction
    def get_new_worker(self, tid):
        return self.worker_class(tid, self.context)

    def start(self, root_url, num_pages):
        self.context.page_limit = num_pages
        self.context.pubsub.push(root_url)
        for worker in self.workers:
            worker.start()
        self.ticker.start()

    def join(self):
        self.ticker.join()
        for worker in self.workers:
            worker.join()

        self.context.pubsub.print_info()


if __name__ == '__main__':
    c = BaseController(10)
    c.start('https://en.wikipedia.org/wiki/Main_Page')
    c.join()
