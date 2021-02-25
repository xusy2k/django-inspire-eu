"""================
Default Settings
================

INSPIRE_EU_DEFAULT_SRID
-----------------------

.. code-block:: python

    INSPIRE_EU_DEFAULT_SRID = settings.INSPIRE_EU_DEFAULT_SRID

INSPIRE_EU_THEMES
-----------------

.. code-block:: python

    INSPIRE_EU_THEMES = {
        "cadastral_parcels": True,
        "buildings": True,
    }

"""
import logging

from django.conf import settings
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

log = logging.getLogger(__name__)

try:
    INSPIRE_EU_DEFAULT_SRID = settings.INSPIRE_EU_DEFAULT_SRID
except AttributeError:
    INSPIRE_EU_DEFAULT_SRID = 4326

try:
    INSPIRE_EU_THEMES = settings.INSPIRE_EU_THEMES
except AttributeError:
    INSPIRE_EU_THEMES = {
        "cadastral_parcels": True,
        "buildings": True,
    }


from .core import (  # noqa
    ApplicationSchema,
    BaseInspireEUModel,
    CodeList,
    CodeListValue,
    Namespace,
    Status,
    Theme,
    UnitOfMeasure,
)
