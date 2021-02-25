import logging

from django.contrib.gis import admin

from . import CadastralParcel, CadastralZoning

log = logging.getLogger(__name__)


@admin.register(CadastralZoning)
class CadastralZoningAdmin(admin.OSMGeoAdmin):
    pass


@admin.register(CadastralParcel)
class CadastralParcelAdmin(admin.OSMGeoAdmin):
    pass
