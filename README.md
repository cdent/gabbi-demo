
# Gabbi Demo

This repo contains a WSGI application that simultaneously operates
as a tool for doing a demo of [gabbi](http://gabbi.readthedocs.org/)
and a tutorial for using gabbi as a tool for doing test driven
development of an API. By viewing the commit history of the
repository you can witness the steps necessary to use gabbi.

Because gabbi was born in the [OpenStack](http://www.openstack.org/)
universe this demo uses some (but not all) of the Python environment
tropes used there (tox, testr, subunit, etc). With luck other demos
will come along for other environments.

# The App

The app that will be created is a simple API that supports storing and
retrieving objects of stuff put in containers. The containers and
objects can have names if you provide them or the server can provide a
name. There is no persistence: data is stored in memory and when the
server shuts down stuff is gone. Fleshing out this rather ambiguous
description is what the testing will do.

For the sake of transparency, the app will not some obscuring
magical framework. Instead [selector](https://pypi.python.org/pypi/selector)
will be used for dispatch and
[WebOb](https://pypi.python.org/pypi/WebOb) for request object
helper methods. This isn't necessarily an ideal setup but it is
simple and that's the point.

# Contributing

Please use GitHub's issues if you have one to report and make a pull
request if you've got something you'd like to add or have a bug fix.
