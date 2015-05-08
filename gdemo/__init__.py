"""
A simple web app to demonstrate storage and retrieval.

This is not meant to demonstrate WSGI app best practice!
"""

import pkg_resources

from gdemo import selector

URLS_MAP = pkg_resources.resource_filename('gdemo', 'urls.map')
FRONT_PAGE = pkg_resources.resource_filename('gdemo', 'frontpage.html')


def load_app():
    return selector.Selector(mapfile=URLS_MAP)


def get_root(environ, start_response):
    start_response('200 OK',
                   [('Content-Type', 'text/html; charset=UTF-8')])
    frontpage = open(FRONT_PAGE, 'rb')
    return frontpage


application = load_app()
