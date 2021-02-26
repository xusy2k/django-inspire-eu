# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    # url(r"^inspire_eu/", include("inspire_eu.urls", namespace="inspire_eu")),
]
