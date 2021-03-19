==================
Django Inspire EU
==================

.. image:: https://img.shields.io/badge/django-2.0,%202.1,%202.2,%203.0,%203.1-092E20.svg
    :target: https://www.djangoproject.com
    :alt: Django 2.0, 2.1, 2.2, 3.0, 3.1
.. image:: https://readthedocs.org/projects/django-inspire-eu/badge/?version=latest
    :target: https://django-inspire-eu.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
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

    * Stable version, preferably within a virtual environment:

            $ mkvirtualenv django-inspire-eu
            $ pip install django-inspire-eu

    * Development version:

        .. code-block:: bash

            $ pip install -e git+https://github.com/xusy2k/django-inspire-eu.git@master#egg=django-inspire_eu


#. Add it to your `INSTALLED_APPS`:

    .. code-block:: python

        INSTALLED_APPS = (
            ...
            "inspire_eu.apps.InspireEuConfig",
            ...
        )

#. Customize :doc:`settings <settings>`

    * :ref:`settings:``INSPIRE_EU_THEMES```
    * :ref:`settings:``INSPIRE_EU_DEFAULT_SRID```
    * :ref:`settings:``INSPIRE_EU_BASE_MODEL```
    * :ref:`settings:``MIGRATION_MODULES```: **Very important** if you want avoid problems with migrations files

#. Make and execute migrations:

    .. code-block:: bash

        python manage.py makemigrations
        python manage.py migrate


#. Populate base models:

    This django command fetch values from https://inspire.ec.europa.eu. In particular: Status:
    (`valid <https://inspire.ec.europa.eu/registry/status/valid>`_, `invalid <https://inspire.ec.europa.eu/registry/status/invalid>`_,
    `retired <https://inspire.ec.europa.eu/registry/status/retired>`_), `Theme <https://inspire.ec.europa.eu/theme/>`_,
    `Application Schema <https://inspire.ec.europa.eu/applicationschema/>`_,
    `Code List <https://inspire.ec.europa.eu/codelist/>`_ and For each Code List key, fetch all its Code List Values

    .. code-block:: bash

        python manage.py load_initial_inspire [-l <language>]  # Default: en


#. Add Django Inspire EU's URL patterns:

    .. code-block:: python

        from inspire_eu import urls as inspire_eu_urls

        urlpatterns = [
            ...
            url(r"^", include(inspire_eu_urls)),
            ...
        ]



Working example
---------------

Follow steps at `django-example directory <https://github.com/xusy2k/django-inspire-eu/tree/master/django-example/>`_


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
