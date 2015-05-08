"""Share utility functions."""

from urllib import parse


def get_route_value(environ, name):
    value = environ['wsgiorg.routing_args'][1][name]
    value = parse.unquote(value)
    return value.replace('%2F', '/')
