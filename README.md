
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

# Tutorial

If you'd like to use this repo as a tutorial the most direct way is
to clone it and then inspect the commit log in reverse:

    git log --reverse

or

    git log -u --reverse

That will tell the story of how the app was built.

# The App

The app that was created is a simple API that supports storing and
retrieving objects of stuff put in containers. The containers and
objects can have names if you provide them or the server can provide a
uuid. There is no persistence: data is stored in memory and when the
server shuts down stuff is gone. The HTML provided at / provides a
list of available URLS. So does the files `gdemo/urls.map`.

For the sake of transparency, the app does not use an obscuring
magical framework. Instead [selector](https://pypi.python.org/pypi/selector)
will be used for dispatch and
[WebOb](https://pypi.python.org/pypi/WebOb) for request object
helper methods. This isn't necessarily a best in business setup but it
is simple and that's the point.

# The Demo

The process used to create the app has resulted in the backend that
will be used during a demo to be given at the OpenStack Liberty
Summit in Vancouver, May 2015. When the artifacts from that presentation
are available they will be linked here.

If you want to run gdemo yourself you need some kind of WSGI server.
[gunicorn](https://pypi.python.org/pypi/gunicorn) works well.
Install it and then from the gdemo repo directory run:

    gunicorn gdemo

Remember your data is just in RAM!

# Contributing

Please use GitHub's issues if you have a problem to report or a suggestion
and make a pull request if you've got something you'd like to add or have
a bug fix.

# Acknowledgements

Thanks to @FND for relaying the idea of using a git history as a
guided learning tool.
