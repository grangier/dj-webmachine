.. _quickstart:

getting started quickly with dj-webmachine
------------------------------------------


Install
+++++++

Make sure that you have a working Python_ 2.x >=2.5 installed and Django_ >= 1.1.


With pip
~~~~~~~~

::
    
    $ pip install dj-webmachine

From source
~~~~~~~~~~~

Get the dj-webmachine code::

    $ git clone https://github.com/benoitc/dj-webmachine.git
    $ cd dj-webmachine

Or using a tarbal::

    $ wget http://github.com/benoitc/dj-webmachine/tarball/master -o dj-webmachine.tar.gz
    $ tar xvzf dj-webmachine.tar.gz
    $ cd dj-webmachine-$HASH/

and install::

    $ sudo python setup.py install


Create a django project
+++++++++++++++++++++++

We will quickly create an Hello world accepting HTML and JSON.

    $ django-admin startproject helloworld
    $ cd helloworld
    $ python manage.py startapp hello

In the hello folder create a file named ``resource.p```:

.. code-block:: python
    
    import json
    from webmachine import Resource
    
    class Hello(Resource):

        def content_types_provided(self, req, resp):
            """" define the content type we render accoridng the Accept
            header.
            """
            return ( 
                ("", self.to_html),
                ("application/json", self.to_json)
            )

        def to_html(self, req, resp):
            return "<html><body>Hello world!</body></html>\n"
    
        def to_json(self, req, resp):
            return "%s\n" % json.dumps({"message": "hello world!", "ok": True})
    
Add **dj-webmachine** and your hello app to ``INSTALLED_APPS`` in your
settings::

    INSTALLED_APPS = (
        ...
        'webmachine',
        'helloworld.hello'
    )

Put your the Hello resource in your ``urls.py``:

.. code-block:: python

    from django.conf.urls.defaults import *

    from helloworld.hello.resources import Hello

    urlpatterns = patterns('',
        (r'^$', Hello()),
    )

Launch your application::

    $ python manage.py runserver

Take a look! Point a web browser at http://localhost:8000/

Or with curl::

    $ curl http://127.0.0.1:8000
    <html><body>Hello world!</body></html>

    $ curl http://127.0.0.1:8000 -H "Accept: application/json"
    {"message": "hello world!", "ok": true}    


    
The first line ask the hello page as html while the second using the
same url ask for JSON. 

To learn how to do more interresting things, checkout :ref:`some examples <examples_resources>` or read :ref:`more documentations <docs>` .

.. _Python: http://python.org
.. _Django: http://djangoproject.org
