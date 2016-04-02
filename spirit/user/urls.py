# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url, include

from .auth import urls as auth_urls
from . import views


urlpatterns = [
    url(r'^$', views.update, name='update'),
    url(r'^avatar-change/$', views.avatar_change, name='avatar-change'),
    url(r'^password-change/$', views.password_change, name='password-change'),
    url(r'^username-change/$', views.username_change, name='username-change'),
    url(r'^email-change/$', views.email_change, name='email-change'),
    url(r'^email-change/(?P<token>[0-9A-Za-z_\-\.]+)/$', views.email_change_confirm, name='email-change-confirm'),

    url(r'^(?P<pk>\d+)/$', views.comments, kwargs={'slug': "", }, name='detail'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.comments, name='detail'),

    url(r'^topics/(?P<pk>\d+)/$', views.topics, kwargs={'slug': "", }, name='topics'),
    url(r'^topics/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.topics, name='topics'),

    url(r'^likes/(?P<pk>\d+)/$', views.likes, kwargs={'slug': "", }, name='likes'),
    url(r'^likes/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.likes, name='likes'),

    url(r'^likes-received/(?P<pk>\d+)/$', views.likes_received, kwargs={'slug': "", }, name='likes-received'),
    url(r'^likes-received/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.likes_received, name='likes-received'),

    url(r'^list/$', views.user_list, name='list'),

    url(r'^menu/$', views.menu, name='menu'),

    url(r'^', include(auth_urls, namespace='auth')),
]
