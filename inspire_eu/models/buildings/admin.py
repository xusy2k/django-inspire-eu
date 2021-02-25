import logging

from django.contrib.gis import admin

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
class BuildingAdmin(admin.OSMGeoAdmin):
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
