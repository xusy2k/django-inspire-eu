import logging

from django.contrib import admin

from ..models import (
    INSPIRE_EU_THEMES,
    ApplicationSchema,
    CodeList,
    CodeListValue,
    Namespace,
    Status,
    Theme,
    UnitOfMeasure,
)

log = logging.getLogger(__name__)


@admin.register(ApplicationSchema)
class ApplicationSchemaAdmin(admin.ModelAdmin):
    pass


@admin.register(CodeList)
class CodeListAdmin(admin.ModelAdmin):
    pass


@admin.register(CodeListValue)
class CodeListValueAdmin(admin.ModelAdmin):
    pass


@admin.register(Namespace)
class NamespaceAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    pass


@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    pass


if "cadastral_parcels" in INSPIRE_EU_THEMES and INSPIRE_EU_THEMES["cadastral_parcels"]:
    from ..models.cadastral_parcels.admin import *  # noqa

if "buildings" in INSPIRE_EU_THEMES and INSPIRE_EU_THEMES["buildings"]:
    from ..models.buildings.admin import *  # noqa
