"""
A simple web app to demonstrate storage and retrieval.

This is not meant to demonstrate WSGI app best practice!
"""

import json
import pkg_resources
import uuid

import webob

from gdemo import selector

URLS_MAP = pkg_resources.resource_filename('gdemo', 'urls.map')
FRONT_PAGE = pkg_resources.resource_filename('gdemo', 'frontpage.html')

DATA_STORE = {}

def load_app():
    return selector.Selector(mapfile=URLS_MAP)


def create_container(environ, start_response):
    request = webob.Request(environ)
    data = json.loads(request.body.decode('UTF-8'))
    container_id = str(uuid.uuid4())

    DATA_STORE[container_id] = data

    location = request.relative_url(container_id)

    start_response('201 Created',
                   [('Location', location)])

    return []


def get_root(environ, start_response):
    start_response('200 OK',
                   [('Content-Type', 'text/html; charset=UTF-8')])
    frontpage = open(FRONT_PAGE, 'rb')
    return frontpage


application = load_app()
