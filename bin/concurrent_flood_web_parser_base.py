from bin.base_controller import BaseController
from bin.base_parser import BaseParser


# easy way to extend functionality
class BaseConcurrentParser:
    parser_class = BaseParser

    def __init__(self, root, num_workers, num_pages):
        self.controller = BaseController(num_workers)
        self.controller.worker_class.parse_class = self.parser_class
        self.root = root
        self.num_pages = num_pages

    def start(self):
        self.controller.start(self.root, self.num_pages)

    def join(self):
        self.controller.join()
