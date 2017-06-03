# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admins/$', views.index_admins, name='index-admins'),
    url(r'^mods/$', views.index_mods, name='index-mods'),
    url(r'^unactive/$', views.index_unactive, name='index-unactive'),
    url(r'^suspended/$', views.index_suspended, name='index-suspended'),
    url(r'^suspensionlog/$', views.index_suspensionlog, name='index-suspensionlog'),
    url(r'^edit/(?P<user_id>\d+)/$', views.edit, name='edit'),
    url(r'^suspend/(?P<user_id>\d+)/$', views.suspend, name='suspend'),
    url(r'^suspend-and-delete/(?P<user_id>\d+)/$', views.suspend_and_delete, name='suspend-and-delete'),
]
