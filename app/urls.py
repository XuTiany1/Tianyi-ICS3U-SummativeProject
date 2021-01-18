# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # Directs the user to the pages function on views.py 
    re_path(r'^.*\.html', views.pages, name='pages'),

    # Directs the user to the index funxtion on views.py
    path('', views.index, name='home'),
]
