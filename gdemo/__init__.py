"""
A simple web app to demonstrate storage and retrieval.

This is not meant to demonstrate WSGI app best practice!
"""

import json
import pkg_resources
import uuid
from urllib import parse

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

    DATA_STORE[container_id] = {
        'owner': data['owner'],
        'objects': []
    }

    location = request.relative_url(container_id)

    start_response('201 Created',
                   [('Location', location)])

    return []


def get_container(environ, start_response):
    container_id = _get_route_value(environ, 'container_id')

    try:
        container = DATA_STORE[container_id]
    except KeyError:
        start_response('404 Not Found', [])
        return []

    data = json.dumps({'owner': container['owner']})

    start_response('200 OK',
                   [('Content-Type', 'application/json')])

    return [data.encode('UTF-8')]


def get_root(environ, start_response):
    start_response('200 OK',
                   [('Content-Type', 'text/html; charset=UTF-8')])
    frontpage = open(FRONT_PAGE, 'rb')
    return frontpage


def update_container(environ, start_response):
    container_id = _get_route_value(environ, 'container_id')
    request = webob.Request(environ)
    data = json.loads(request.body.decode('UTF-8'))

    if container_id in DATA_STORE:
        response_code = '204 No Content'
        DATA_STORE[container_id]['owner'] = data['owner']
    else:
        response_code = '201 Created'
        DATA_STORE[container_id] = {
            'owner': data['owner'],
            'objects': []
        }

    location = request.relative_url(container_id)

    start_response(response_code,
                   [('Location', location)])

    return []


def _get_route_value(environ, name):
    value = environ['wsgiorg.routing_args'][1][name]
    value = parse.unquote(value)
    return value.replace('%2F', '/')


application = load_app()
