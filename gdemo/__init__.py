"""
A simple web app to demonstrate storage and retrieval.
"""

import pkg_resources
import selector

URLS_MAP = pkg_resources.resource_filename('gdemo', 'urls.map')


def load_app():
    return selector.Selector(mapfile=URLS_MAP)


def get_root(environ, start_response):
    start_response('200 OK',
                   [('Content-Type', 'text/html; charset=UTF-8')])
    return [b'Hello World\n']


application = load_app()
