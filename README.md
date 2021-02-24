Django Inspire EU
=================

[![Django 2.X](https://img.shields.io/badge/django-2.X-092E20.svg)](https://www.djangoproject.com)
[![image](https://badge.fury.io/py/django-inspire-eu.svg)](https://badge.fury.io/py/django-inspire-eu)
[![See Build Status on Travis CI](https://travis-ci.com/xusy2k/django-inspire-eu.svg?branch=master)](https://travis-ci.com/xusy2k/django-inspire-eu)
[![image](https://codecov.io/gh/xusy2k/django-inspire-eu/branch/master/graph/badge.svg)](https://codecov.io/gh/xusy2k/django-inspire-eu)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

This package is the django implementation from the
[themes](https://inspire.ec.europa.eu/Themes/Data-Specifications/2892)
of the infrastructure for spatial information in Europe (INSPIRE)

Documentation
-------------

The full documentation is at <https://django-inspire-eu.readthedocs.io>.

Quickstart
----------

1.  Install Django Inspire EU:

    > ``` {.sourceCode .bash}
    > $ pip install -e git+https://github.com/xusy2k/django-inspire-eu.git@master#egg=django-inspire_eu
    > ```

2.  Add it to your \`INSTALLED\_APPS\`:

    > ``` {.sourceCode .python}
    > INSTALLED_APPS = (
    >     ...
    >     'inspire_eu.apps.InspireEuConfig',
    >     ...
    > )
    > ```

3.  Add Django Inspire EU's URL patterns:

    > ``` {.sourceCode .python}
    > from inspire_eu import urls as inspire_eu_urls
    >
    > urlpatterns = [
    >     ...
    >     url(r'^', include(inspire_eu_urls)),
    >     ...
    > ]
    > ```

4.  Make and execute migrations:

    > ``` {.sourceCode .bash}
    > python manage.py makemigrations
    > python manage.py migrate
    > ```

5.  Populate base models:

This django command fetch values from <https://inspire.ec.europa.eu>. In
particular: Status:
([valid](https://inspire.ec.europa.eu/registry/status/valid),
[invalid](https://inspire.ec.europa.eu/registry/status/invalid),
[retired](https://inspire.ec.europa.eu/registry/status/retired)),
[Theme](https://inspire.ec.europa.eu/theme/theme.en.json), [Application
Schema](https://inspire.ec.europa.eu/applicationschema/applicationschema.en.json),
[Code List](https://inspire.ec.europa.eu/codelist/codelist.en.atom) and
For each Code List key, fetch all its Code List Values

> ``` {.sourceCode .bash}
> python manage.py load_initial_inspire [-l <language>]  # Default: en
> ```

Running Tests
-------------

Does the code actually work?

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Development commands
--------------------

    pip install -r requirements_dev.txt
    invoke -l

Credits
-------

Tools used in rendering this package:

-   [Cookiecutter](https://github.com/audreyr/cookiecutter)
-   [cookiecutter-djangopackage](https://github.com/pydanny/cookiecutter-djangopackage)
