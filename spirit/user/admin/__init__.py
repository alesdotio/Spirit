# -*- coding: utf-8 -*-

from __future__ import unicode_literals

default_app_config = 'spirit.user.admin.apps.SpiritUserAdminConfig'


from django.contrib import admin
from ..models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username',)
    list_display = ('__str__', 'last_seen', 'is_verified', 'is_administrator', 'is_moderator')
    raw_id_fields = ('user',)


admin.site.register(UserProfile, UserProfileAdmin)
