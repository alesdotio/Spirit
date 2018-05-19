# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

import pytz
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import ugettext as _

from djconfig import config

from spirit.user.models import UserSuspensionLog
from ...core.utils.paginator import yt_paginate
from ...core.utils.decorators import administrator_required, moderator_required
from .forms import UserForm, UserProfileForm, UserSuspendForm, UserSuspendAndDeleteForm

User = get_user_model()


@administrator_required
def edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        uform = UserForm(data=request.POST, instance=user)
        form = UserProfileForm(data=request.POST, instance=user.st)

        if all([uform.is_valid(), form.is_valid()]):
            uform.save()
            form.save()
            messages.info(request, _("This profile has been updated!"))
            return redirect(request.GET.get("next", request.get_full_path()))
    else:
        uform = UserForm(instance=user)
        form = UserProfileForm(instance=user.st)

    context = {
        'form': form,
        'uform': uform
    }

    return render(request, 'spirit/user/admin/edit.html', context)


@moderator_required
def suspend(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if user.is_superuser or user.is_staff or user.st.is_administrator or user.st.is_moderator:
        messages.error(request, _("You cannot suspend another administrator or moderator!"))
        return redirect(user.st.get_absolute_url())

    if request.method == 'POST':
        form = UserSuspendForm(data=request.POST, instance=user.st)

        if form.is_valid():
            form.save()
            UserSuspensionLog.objects.create(
                user=user,
                suspended_by=request.user,
                suspended_until=form.cleaned_data['is_suspended_until'],
                suspension_reason=form.cleaned_data['suspension_reason'],
            )
            messages.info(request, _("User suspension has been updated!"))
            return redirect(user.st.get_absolute_url())
    else:
        form = UserSuspendForm(instance=user.st)

    context = {
        'form': form,
        'p_user': user
    }

    return render(request, 'spirit/user/admin/suspend.html', context)


@moderator_required
def suspend_and_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if user.is_superuser or user.is_staff or user.st.is_administrator or user.st.is_moderator:
        messages.error(request, _("You cannot suspend another administrator or moderator!"))
        return redirect(user.st.get_absolute_url())

    if user.date_joined < timezone.now() - datetime.timedelta(days=3):
        messages.error(request, _("You cannot delete a user older than 3 days!"))
        return redirect(user.st.get_absolute_url())

    if request.method == 'POST':
        form = UserSuspendAndDeleteForm(data=request.POST)

        if form.is_valid():
            suspend_until = pytz.UTC.localize(datetime.datetime(3000, 1, 1))

            # suspend user
            user.st.is_suspended_until = suspend_until
            user.st.suspension_reason = form.cleaned_data['suspension_reason']
            user.st.save()

            # delete topics and comments
            user.st_topics.exclude(is_removed=True).update(is_removed=True, reindex_at=timezone.now())
            user.st_comments.update(is_removed=True)

            # log suspension
            UserSuspensionLog.objects.create(
                user=user,
                suspended_by=request.user,
                suspended_until=suspend_until,
                suspension_reason=form.cleaned_data['suspension_reason'],
            )
            messages.info(request, _("User has been suspended and all comments have been deleted!"))
            return redirect(user.st.get_absolute_url())
    else:
        form = UserSuspendAndDeleteForm()

    context = {
        'form': form,
        'p_user': user,
        'comments_num': user.st_comments.count(),
        'topics_num': user.st_topics.count(),
    }

    return render(request, 'spirit/user/admin/suspend_and_delete.html', context)


@moderator_required
def _index(request, queryset, template):
    users = yt_paginate(
        queryset.order_by('-date_joined', '-pk'),
        per_page=config.topics_per_page,
        page_number=request.GET.get('page', 1)
    )
    context = {'users': users, }
    return render(request, template, context)


def index(request):
    return _index(
        request,
        queryset=User.objects.all(),
        template='spirit/user/admin/index.html'
    )


def index_admins(request):
    return _index(
        request,
        queryset=User.objects.filter(st__is_administrator=True),
        template='spirit/user/admin/admins.html'
    )


def index_mods(request):
    return _index(
        request,
        queryset=User.objects.filter(st__is_moderator=True, st__is_administrator=False),
        template='spirit/user/admin/mods.html'
    )


def index_unactive(request):
    return _index(
        request,
        queryset=User.objects.filter(is_active=False),
        template='spirit/user/admin/unactive.html'
    )


def index_suspended(request):
    return _index(
        request,
        queryset=User.objects.filter(is_active=True, st__is_suspended_until__gt=timezone.now().today()),
        template='spirit/user/admin/suspended.html'
    )


@moderator_required
def index_suspensionlog(request):
    suspensionlogs = yt_paginate(
        UserSuspensionLog.objects.all(),
        per_page=50,
        page_number=request.GET.get('page', 1)
    )
    context = {'suspensionlogs': suspensionlogs, }
    return render(request, 'spirit/user/admin/suspensionlog.html', context)
