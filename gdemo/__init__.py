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
        'objects': {}
    }

    location = request.relative_url(container_id)

    start_response('201 Created',
                   [('Location', location)])

    return []


def delete_container(environ, start_response):
    container_id = _get_route_value(environ, 'container_id')

    try:
        del DATA_STORE[container_id]
    except KeyError:
        start_response('404 Not Found', [])
        return []

    start_response('204 No Content', [])
    return []


def delete_object(environ, start_response):
    container_id = _get_route_value(environ, 'container_id')
    object_id = _get_route_value(environ, 'object_id')

    try:
        del DATA_STORE[container_id]['objects'][object_id]
    except KeyError:
        start_response('404 Not Found', [])
        return []

    start_response('204 No Content', [])
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


def get_object(environ, start_response):
    container_id = _get_route_value(environ, 'container_id')
    object_id = _get_route_value(environ, 'object_id')

    try:
        object = DATA_STORE[container_id]['objects'][object_id]
    except KeyError:
        start_response('404 Not Found', [])
        return []

    start_response('200 OK',
                   [('Content-Type', object['type'])])
    return [object['body']]


def get_root(environ, start_response):
    start_response('200 OK',
                   [('Content-Type', 'text/html; charset=UTF-8')])
    frontpage = open(FRONT_PAGE, 'rb')
    return frontpage


def list_objects(environ, start_response):
    request = webob.Request(environ)
    best_match = request.accept.best_match(['application/json', 'text/plain'])
    container_id = _get_route_value(environ, 'container_id')

    try:
        objects = DATA_STORE[container_id]['objects']
    except KeyError:
        start_response('404 Not Found', [])
        return []

    objects = sorted(objects.keys())
    # container-ize the objects to avoid top level json list
    if best_match == 'application/json':
        data = json.dumps({'objects': objects})
    elif best_match == 'text/plain':
        data = '\n'.join(objects)
    else:
        start_response('406 Not Acceptable', [])
        return []

    start_response('200 OK',
                   [('Content-Type', '%s; charset=UTF-8' % best_match)])

    return [data.encode('UTF-8')]


def create_object(environ, start_response):
    container_id = _get_route_value(environ, 'container_id')
    object_id = str(uuid.uuid4())
    request = webob.Request(environ)

    object_data = {
        'type': request.content_type,
        'body': request.body  # no encoding handling
    }

    try:
        DATA_STORE[container_id]['objects'][object_id] = object_data
    except KeyError:
        start_response('404 Not Found', [])
        return []

    location = request.relative_url('objects/%s' % object_id)

    start_response('201 Created',
                   [('Location', location)])

    return []


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
            'objects': {}
        }

    location = request.url

    start_response(response_code,
                   [('Location', location)])

    return []


def update_object(environ, start_response):
    container_id = _get_route_value(environ, 'container_id')
    object_id = _get_route_value(environ, 'object_id')
    request = webob.Request(environ)

    object_data = {
        'type': request.content_type,
        'body': request.body  # no encoding handling
    }

    if object_id in DATA_STORE[container_id]['objects']:
        status = '204 No Content'
    else:
        status = '201 Created'

    try:
        DATA_STORE[container_id]['objects'][object_id] = object_data
    except KeyError:
        start_response('404 Not Found', [])
        return []

    location = request.url

    start_response(status,
                   [('Location', location)])

    return []


def _get_route_value(environ, name):
    value = environ['wsgiorg.routing_args'][1][name]
    value = parse.unquote(value)
    return value.replace('%2F', '/')


application = load_app()
