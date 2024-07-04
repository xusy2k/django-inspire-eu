import logging

from django.contrib.gis import admin

try:
    # Django < 4.0
    # https://code.djangoproject.com/ticket/27674
    GISModelAdmin = admin.OSMGeoAdmin
except AttributeError:
    GISModelAdmin = admin.GISModelAdmin

from . import CadastralParcel, CadastralZoning

log = logging.getLogger(__name__)


@admin.register(CadastralZoning)
class CadastralZoningAdmin(GISModelAdmin):
    pass


@admin.register(CadastralParcel)
class CadastralParcelAdmin(GISModelAdmin):
    pass
