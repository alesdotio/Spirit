from django.views.generic import DetailView, ListView, TemplateView
from spirit.core.utils.paginator import paginate
from spirit.topic.models import Topic
from spirit.topic.tag.models import TopicTag


class TagList(ListView):
    template_name = 'spirit/topic/tag/tag_list.html'
    model = TopicTag

    def get_context_data(self, **kwargs):
        ctx = super(TagList, self).get_context_data(**kwargs)
        ctx.update({
            'pinned_slug': 'pinned',
            'pinned_name': 'Pinned',
            'pinned_description': 'Topics that are pinned to the top',
        })
        return ctx


class TagPinnedDetail(TemplateView):
    template_name = 'spirit/topic/tag/tag_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super(TagPinnedDetail, self).get_context_data(**kwargs)

        topics = Topic.objects\
            .visible(self.request.user)\
            .with_bookmarks(user=self.request.user)\
            .filter(is_pinned=True)\
            .order_by('-is_globally_pinned', '-is_pinned', '-last_active')\
            .select_related('user', 'user__st', 'last_commenter', 'last_commenter__st')\
            .prefetch_related('topictagrelation_set', 'topictagrelation_set__tag')\

        topics = paginate(
            topics,
            per_page=20,
            page_number=self.request.GET.get('page', 1)
        )
        ctx.update({
            'tag': {
                'slug': 'pinned',
                'name': 'Pinned',
                'description': 'Topics that are pinned to the top',
            },
            'topics': topics,
        })
        return ctx


class TagDetail(DetailView):
    template_name = 'spirit/topic/tag/tag_detail.html'
    model = TopicTag
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        ctx = super(TagDetail, self).get_context_data(**kwargs)
        tag = self.object

        topics = Topic.objects\
            .visible(self.request.user)\
            .with_bookmarks(user=self.request.user)\
            .order_by('-is_globally_pinned', '-is_pinned', '-last_active')\
            .select_related('user', 'user__st', 'last_commenter', 'last_commenter__st')\
            .prefetch_related('topictagrelation_set', 'topictagrelation_set__tag')\
            .filter(topictagrelation_set__tag_id=tag.pk)

        topics = paginate(
            topics,
            per_page=20,
            page_number=self.request.GET.get('page', 1)
        )
        ctx.update({
            'tag': tag,
            'topics': topics,
        })
        return ctx
