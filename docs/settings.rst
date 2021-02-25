========
Settings
========

This package is intended to run smoothly out of the box once it is installed.
However we can find ourselves in the situation that the current implementation
does not suit our needs.
To solve this problem some settings have been considered that can help us to
customize the package according to our needs.

These are the variables can be customized through ``settings.py``:

.. code-block:: python

    # settings.py
    INSPIRE_EU_THEMES = {
        "cadastral_parcels": True,
        "buildings": True,
    }
    INSPIRE_EU_DEFAULT_SRID = 4326
    INSPIRE_EU_BASE_MODEL = "full.path.to.your.base_model"  # Optional


Above, the default values for these settings are shown.


``INSPIRE_EU_THEMES``
---------------------

It is a dictionary that contains the list of themes to be installed. The default value is **True** but in case you don't install some of them
you can set to False.

For instance, if you only want to install the :doc:`Cadastral parcels theme <theme/cadastral_parcels/index>` you could define it as:

.. code-block:: python

    # settings.py
    INSPIRE_EU_THEMES = {
        "cadastral_parcels": True,
        "buildings": False,
    }


``INSPIRE_EU_DEFAULT_SRID``
---------------------------

Sets the SRID (Spatial Reference System Identity) of all geometry fields to the given value. Defaults to `4326 <https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84>`_
(also known as WGS84, units are in degrees of longitude and latitude).


``INSPIRE_EU_BASE_MODEL``
-------------------------

It is an abstract model to facilitate the addition of fields or features that will be included in each and every one of the models.

For instance, if you would add an ``uuid`` field you could define like this:

.. code-block:: python

    # settings.py
    INSPIRE_EU_BASE_MODEL = "my_awesome_app.models.ExampleBaseModel"

    # my_awesome_app/models.py
    import uuid as uuid_lib
    from django.contrib.gis.db import models

    class ExampleBaseModel(models.Model):
        uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)

        class Meta:
            abstract = True  # VERY IMPORTANT!


``MIGRATION_MODULES``
---------------------

The best solution for use this package it is reuse all base code but keeping safe the migrations files inside our project.
To achieve it Django provide us the setting `MIGRATION_MODULES <https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-MIGRATION_MODULES>`_
that it's a dictionary specifying the package where migration modules can be found on a per-app basis.

    .. code-block:: python

        # settings.py
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-MIGRATION_MODULES
        MIGRATION_MODULES = {
            "inspire_eu": "my_awesome_app.migrations_inspire_eu"  # Recomendable
        }

.. warning::

    Any changes about this settings must be followed by the migrations commands:

    .. code-block:: bash

        python manage.py makemigrations
        pythom manage.py migrate

