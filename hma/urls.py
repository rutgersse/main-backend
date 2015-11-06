"""hma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from hma.models import *

admin.site.register(Location)

admin.site.register(Activity)


urlpatterns = [
	url( r'^$', 'hma.views.index', name='index' ),
    url(r'^admin/', include(admin.site.urls)),
    url( r'^location/all/$', 'hma.views.location_all', name='all location' ),
    url( r'^activity/all/$', 'hma.views.activity_all', name='all activity' ),
    url( r'^location/(?P<entity_slug>[a-zA-Z0-9_.-]+)/$', 'hma.views.location', name='location' ),
    url( r'^activity/(?P<entity_slug>[a-zA-Z0-9_.-]+)/$', 'hma.views.activity', name='activity' ),

    # (?P<entity_slug>[a-zA-Z0-9_.-]+)
    # url( r'^$', 'hma.views.index', name='index' ),
    # url( r'^$', 'hma.views.index', name='index' ),
    # url( r'^$', 'hma.views.index', name='index' ),
]
