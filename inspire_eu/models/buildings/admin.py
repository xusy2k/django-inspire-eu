import logging

from django.contrib.gis import admin

try:
    # Django < 4.0
    # https://code.djangoproject.com/ticket/27674
    GISModelAdmin = admin.OSMGeoAdmin
except AttributeError:
    GISModelAdmin = admin.GISModelAdmin

from . import (
    Building,
    BuildingCurrentUse,
    BuildingDocument,
    BuildingElevation,
    BuildingExternalReference,
    BuildingGeographicalName,
    BuildingHeightAboveGround,
    BuildingNature,
    OtherConstruction,
)

log = logging.getLogger(__name__)


@admin.register(Building)
class BuildingAdmin(GISModelAdmin):
    pass


@admin.register(BuildingDocument)
class BuildingDocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(BuildingElevation)
class BuildingElevationAdmin(admin.ModelAdmin):
    pass


@admin.register(BuildingExternalReference)
class BuildingExternalReferenceAdmin(admin.ModelAdmin):
    pass


@admin.register(BuildingHeightAboveGround)
class BuildingHeightAboveGroundAdmin(admin.ModelAdmin):
    pass


@admin.register(BuildingNature)
class BuildingNatureAdmin(admin.ModelAdmin):
    pass


@admin.register(BuildingCurrentUse)
class BuildingCurrentUseAdmin(admin.ModelAdmin):
    pass


@admin.register(BuildingGeographicalName)
class BuildingGeographicalNameAdmin(admin.ModelAdmin):
    pass


@admin.register(OtherConstruction)
class OtherConstructionAdmin(admin.ModelAdmin):
    pass
