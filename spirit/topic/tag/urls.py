from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^list/$', views.TagList.as_view(), name='list'),
    url(r'^pinned/$', views.TagPinnedDetail.as_view(), name='pinned'),
    url(r'^(?P<slug>[\w-]+)/$', views.TagDetail.as_view(), name='detail'),
]
