"""Handlers for objects in gdemo."""

import json
import uuid

import webob

from gdemo import DATA_STORE
from gdemo.util import get_route_value


def get_object(environ, start_response):
    container_id = get_route_value(environ, 'container_id')
    object_id = get_route_value(environ, 'object_id')

    try:
        object = DATA_STORE[container_id]['objects'][object_id]
    except KeyError:
        start_response('404 Not Found', [])
        return []

    start_response('200 OK',
                   [('Content-Type', object['type'])])
    return [object['body']]


def create_object(environ, start_response):
    container_id = get_route_value(environ, 'container_id')
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


def update_object(environ, start_response):
    container_id = get_route_value(environ, 'container_id')
    object_id = get_route_value(environ, 'object_id')
    request = webob.Request(environ)

    object_data = {
        'type': request.content_type,
        'body': request.body  # no encoding handling
    }

    try:
        if object_id in DATA_STORE[container_id]['objects']:
            status = '204 No Content'
        else:
            status = '201 Created'

        DATA_STORE[container_id]['objects'][object_id] = object_data
    except KeyError:
        start_response('404 Not Found', [])
        return []

    location = request.url

    start_response(status,
                   [('Location', location)])

    return []


def delete_object(environ, start_response):
    container_id = get_route_value(environ, 'container_id')
    object_id = get_route_value(environ, 'object_id')

    try:
        del DATA_STORE[container_id]['objects'][object_id]
    except KeyError:
        start_response('404 Not Found', [])
        return []

    start_response('204 No Content', [])
    return []


def list_objects(environ, start_response):
    request = webob.Request(environ)
    best_match = request.accept.best_match(['application/json', 'text/plain'])
    container_id = get_route_value(environ, 'container_id')

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
