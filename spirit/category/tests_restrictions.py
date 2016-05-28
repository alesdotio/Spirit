# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import Group

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.cache import cache

from ..core.tests import utils
from spirit.comment.models import Comment
from ..topic.models import Topic
from .models import Category


class CategoryViewTest(TestCase):

    def setUp(self):
        cache.clear()
        self.user = utils.create_user()
        self.category_1 = utils.create_category(title="cat1")
        self.subcategory_1 = utils.create_subcategory(self.category_1)
        self.category_2 = utils.create_category(title="cat2")
        self.category_removed = utils.create_category(title="cat3", is_removed=True)
        self.uncategorized = Category.objects.get(title="Uncategorized")

    def test_category_restrict_access(self):
        """
        Tests a category that only a secret group can access.
        """
        secret_group = Group.objects.create(name='secret group')
        secret_category = utils.create_category(title="restricted")
        secret_category.restrict_access.add(secret_group)
        user_with_access = utils.create_user()
        user_with_access.groups.add(secret_group)
        secret_topic = utils.create_topic(category=secret_category, user=user_with_access, title='secret topic')
        secret_comment = utils.create_comment(topic=secret_topic, user=user_with_access)
        self.assertEqual(Topic.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)

        # should display only categories with no access restriction
        response = self.client.get(reverse('spirit:category:index'))
        self.assertEqual(
            list(response.context['categories']),
            [self.uncategorized, self.category_1, self.category_2]
        )
        utils.login(self)
        response = self.client.get(reverse('spirit:category:index'))
        self.assertEqual(
            list(response.context['categories']),
            [self.uncategorized, self.category_1, self.category_2]
        )

        # cannot create topics
        utils.login(self)
        utils.cache_clear()
        form_data = {'comment': 'foo1', 'title': 'foobar1', 'category': secret_category.pk}
        response = self.client.post(reverse('spirit:topic:publish', kwargs={'category_id': secret_category.pk, }),
                                    form_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Topic.objects.count(), 1)

        # cannot comment
        utils.cache_clear()
        form_data = {'comment': 'foo2', }
        response = self.client.post(reverse('spirit:comment:publish', kwargs={'topic_id': secret_topic.pk, }),
                                    form_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Comment.objects.count(), 1)

        # now login with user that has access
        utils.login(self, user=user_with_access)

        # should display all categories, even access restricted
        response = self.client.get(reverse('spirit:category:index'))
        self.assertEqual(
            list(response.context['categories']),
            [self.uncategorized, self.category_1, self.category_2, secret_category]
        )

        # can create topics
        utils.cache_clear()
        form_data = {'comment': 'foo3', 'title': 'foobar2', 'category': secret_category.pk}
        response = self.client.post(reverse('spirit:topic:publish', kwargs={'category_id': secret_category.pk, }),
                                    form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Topic.objects.count(), 2)

        # can comment
        utils.cache_clear()
        form_data = {'comment': 'foo4', }
        response = self.client.post(reverse('spirit:comment:publish', kwargs={'topic_id': secret_topic.pk, }),
                                    form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 3)

    def test_category_restrict_topic(self):
        """
        Tests a category that only a secret group can create topics in.
        """
        secret_group = Group.objects.create(name='secret group')
        secret_category = utils.create_category(title="restricted")
        secret_category.restrict_topic.add(secret_group)
        user_with_access = utils.create_user()
        user_with_access.groups.add(secret_group)
        secret_topic = utils.create_topic(category=secret_category, user=user_with_access, title='secret topic')
        secret_comment = utils.create_comment(topic=secret_topic, user=user_with_access)
        self.assertEqual(Topic.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)

        # should display all categories
        response = self.client.get(reverse('spirit:category:index'))
        self.assertEqual(
            list(response.context['categories']),
            [self.uncategorized, self.category_1, self.category_2, secret_category]
        )

        # cannot create topics
        utils.login(self)
        utils.cache_clear()
        form_data = {'comment': 'foo5', 'title': 'foobar3', 'category': secret_category.pk}
        response = self.client.post(reverse('spirit:topic:publish', kwargs={'category_id': secret_category.pk, }),
                                    form_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Topic.objects.count(), 1)

        # but can comment
        utils.cache_clear()
        form_data = {'comment': 'foo6', }
        response = self.client.post(reverse('spirit:comment:publish', kwargs={'topic_id': secret_topic.pk, }),
                                    form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 2)

        # now login with user that has access
        utils.login(self, user=user_with_access)

        # should still display all categories
        response = self.client.get(reverse('spirit:category:index'))
        self.assertEqual(
            list(response.context['categories']),
            [self.uncategorized, self.category_1, self.category_2, secret_category]
        )

        # can create topics
        utils.cache_clear()
        form_data = {'comment': 'foo7', 'title': 'foobar4', 'category': secret_category.pk}
        response = self.client.post(reverse('spirit:topic:publish', kwargs={'category_id': secret_category.pk, }),
                                    form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Topic.objects.count(), 2)

        # can comment
        utils.cache_clear()
        form_data = {'comment': 'foo8', }
        response = self.client.post(reverse('spirit:comment:publish', kwargs={'topic_id': secret_topic.pk, }),
                                    form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 4)

    def test_category_restrict_comment(self):
        """
        Tests a category that only a secret group can comment in.
        """
        secret_group = Group.objects.create(name='secret group')
        secret_category = utils.create_category(title="restricted")
        secret_category.restrict_comment.add(secret_group)
        user_with_access = utils.create_user()
        user_with_access.groups.add(secret_group)
        secret_topic = utils.create_topic(category=secret_category, user=user_with_access, title='secret topic')
        secret_comment = utils.create_comment(topic=secret_topic, user=user_with_access)
        self.assertEqual(Topic.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)

        # should display all categories
        response = self.client.get(reverse('spirit:category:index'))
        self.assertEqual(
            list(response.context['categories']),
            [self.uncategorized, self.category_1, self.category_2, secret_category]
        )

        # can create topics
        utils.login(self)
        utils.cache_clear()
        form_data = {'comment': 'foo9', 'title': 'foobar5', 'category': secret_category.pk}
        response = self.client.post(reverse('spirit:topic:publish', kwargs={'category_id': secret_category.pk, }),
                                    form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Topic.objects.count(), 2)

        # but cannot comment
        utils.cache_clear()
        form_data = {'comment': 'foo10', }
        response = self.client.post(reverse('spirit:comment:publish', kwargs={'topic_id': secret_topic.pk, }),
                                    form_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Comment.objects.count(), 2)

        # now login with user that has access
        utils.login(self, user=user_with_access)

        # should still display all categories
        response = self.client.get(reverse('spirit:category:index'))
        self.assertEqual(
            list(response.context['categories']),
            [self.uncategorized, self.category_1, self.category_2, secret_category]
        )

        # can create topics
        utils.cache_clear()
        form_data = {'comment': 'foo11', 'title': 'foobar6', 'category': secret_category.pk}
        response = self.client.post(reverse('spirit:topic:publish', kwargs={'category_id': secret_category.pk, }),
                                    form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Topic.objects.count(), 3)

        # can comment
        utils.cache_clear()
        form_data = {'comment': 'foo12', }
        response = self.client.post(reverse('spirit:comment:publish', kwargs={'topic_id': secret_topic.pk, }),
                                    form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 4)
