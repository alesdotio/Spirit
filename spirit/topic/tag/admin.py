from django.contrib import admin
from spirit.topic.tag.models import TopicTag, TopicTagRelation


class TopicTagAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')

admin.site.register(TopicTag, TopicTagAdmin)


class TopicTagRelationAdmin(admin.ModelAdmin):
    list_display = ('tag', 'topic')
    raw_id_fields = ('topic', )

admin.site.register(TopicTagRelation, TopicTagRelationAdmin)
