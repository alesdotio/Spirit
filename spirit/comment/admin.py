from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'topic', 'date')
    list_filter = ('topic__category',)
    raw_id_fields = ('user', 'topic')


admin.site.register(Comment, CommentAdmin)


from ..topic.models import Topic


class TopicAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'category', 'date', 'user')
    list_filter = ('category',)
    raw_id_fields = ('user',)


admin.site.register(Topic, TopicAdmin)