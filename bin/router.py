import re

from bin.exceptions import RoutingException


# resposible for registering and routing urls
class RouteManager:
    paths = {}

    @staticmethod
    def register(cls, regex):
        RouteManager.paths[re.compile(regex)] = cls

    @staticmethod
    def route(url):
        for regex, cls in RouteManager.paths.items():
            if regex.match(url):
                return cls

        raise RoutingException('No route found for "%s"\n.' % url)


class Route:
    def __init__(self, regex):
        self.regex = regex

    def __call__(self, cls):
        RouteManager.register(cls, self.regex)
        return cls
