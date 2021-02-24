==================
Django Inspire EU
==================

.. image:: https://img.shields.io/badge/django-2.X-092E20.svg
    :target: https://www.djangoproject.com
    :alt: Django 2.X
.. image:: https://badge.fury.io/py/django-inspire-eu.svg
    :target: https://badge.fury.io/py/django-inspire-eu
.. image:: https://travis-ci.com/xusy2k/django-inspire-eu.svg?branch=master
    :target: https://travis-ci.com/xusy2k/django-inspire-eu
    :alt: See Build Status on Travis CI
.. image:: https://codecov.io/gh/xusy2k/django-inspire-eu/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/xusy2k/django-inspire-eu
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Code style: black


This package is the django implementation from the `themes <https://inspire.ec.europa.eu/Themes/Data-Specifications/2892>`_
of the infrastructure for spatial information in Europe (INSPIRE)

Documentation
-------------

The full documentation is at https://django-inspire-eu.readthedocs.io.

Quickstart
----------

#. Install Django Inspire EU:

    .. code-block:: bash

        $ pip install -e git+https://github.com/xusy2k/django-inspire-eu.git@master#egg=django-inspire_eu

    .. At the command line::

    ..     $ easy_install django-inspire-eu

    .. Or, if you have virtualenvwrapper installed::

    ..     $ mkvirtualenv django-inspire-eu
    ..     $ pip install django-inspire-eu


#. Add it to your `INSTALLED_APPS`:

    .. code-block:: python

        INSTALLED_APPS = (
            ...
            'inspire_eu.apps.InspireEuConfig',
            ...
        )

#. Add Django Inspire EU's URL patterns:

    .. code-block:: python

        from inspire_eu import urls as inspire_eu_urls

        urlpatterns = [
            ...
            url(r'^', include(inspire_eu_urls)),
            ...
        ]


#. Make and execute migrations:

    .. code-block:: bash

        python manage.py makemigrations
        python manage.py migrate


#. Populate base models:

This django command fetch values from https://inspire.ec.europa.eu. In particular: Status:
(`valid <https://inspire.ec.europa.eu/registry/status/valid>`_, `invalid <https://inspire.ec.europa.eu/registry/status/invalid>`_,
`retired <https://inspire.ec.europa.eu/registry/status/retired>`_), `Theme <https://inspire.ec.europa.eu/theme/theme.en.json>`_,
`Application Schema <https://inspire.ec.europa.eu/applicationschema/applicationschema.en.json>`_,
`Code List <https://inspire.ec.europa.eu/codelist/codelist.en.atom>`_ and For each Code List key, fetch all its Code List Values

    .. code-block:: bash

        python manage.py load_initial_inspire [-l <language>]  # Default: en


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage