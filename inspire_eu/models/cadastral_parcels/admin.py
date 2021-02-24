import logging

from django.contrib import admin

from . import CadastralParcel, CadastralZoning

log = logging.getLogger(__name__)


@admin.register(CadastralZoning)
class CadastralZoningAdmin(admin.ModelAdmin):
    pass


@admin.register(CadastralParcel)
class CadastralParcelAdmin(admin.ModelAdmin):
    pass
