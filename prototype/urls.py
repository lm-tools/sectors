# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

handler500 = 'prototype.apps.sectors.views.server_error'

urlpatterns = [
    url(r'', include('sectors.urls', namespace='sectors')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
