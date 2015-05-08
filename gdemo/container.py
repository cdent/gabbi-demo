"""Handlers for containers in gdemo."""

import json
import uuid

import webob

from gdemo import DATA_STORE
from gdemo.util import get_route_value


def get_container(environ, start_response):
    container_id = get_route_value(environ, 'container_id')

    try:
        container = DATA_STORE[container_id]
    except KeyError:
        start_response('404 Not Found', [])
        return []

    data = json.dumps({'owner': container['owner']})

    start_response('200 OK',
                   [('Content-Type', 'application/json')])

    return [data.encode('UTF-8')]


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


def update_container(environ, start_response):
    container_id = get_route_value(environ, 'container_id')
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


def delete_container(environ, start_response):
    container_id = get_route_value(environ, 'container_id')

    try:
        del DATA_STORE[container_id]
    except KeyError:
        start_response('404 Not Found', [])
        return []

    start_response('204 No Content', [])
    return []
