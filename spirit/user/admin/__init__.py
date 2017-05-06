# -*- coding: utf-8 -*-

from __future__ import unicode_literals

default_app_config = 'spirit.user.admin.apps.SpiritUserAdminConfig'


from django.contrib import admin
from ..models import UserProfile, UserSuspensionLog


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username',)
    list_display = ('__str__', 'last_seen', 'is_verified', 'is_administrator', 'is_moderator')
    raw_id_fields = ('user',)


admin.site.register(UserProfile, UserProfileAdmin)


class UserSuspensionLogAdmin(admin.ModelAdmin):
    search_fields = ('user__username', )
    list_display = ('__str__', 'date_created', 'suspension_reason')
    raw_id_fields = ('user', 'suspended_by')


admin.site.register(UserSuspensionLog, UserSuspensionLogAdmin)
