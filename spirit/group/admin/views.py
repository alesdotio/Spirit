# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import Group

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from ...core.utils.decorators import administrator_required
from .forms import GroupForm


@administrator_required
def index(request):
    groups = Group.objects.all()
    context = {'groups': groups, }
    return render(request, 'spirit/group/admin/index.html', context)


@administrator_required
def create(request):
    if request.method == 'POST':
        form = GroupForm(data=request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse("spirit:admin:group:index"))
    else:
        form = GroupForm()

    context = {'form': form, }

    return render(request, 'spirit/group/admin/create.html', context)


@administrator_required
def update(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    if request.method == 'POST':
        form = GroupForm(data=request.POST, instance=group)

        if form.is_valid():
            form.save()
            messages.info(request, _("The group has been updated!"))
            return redirect(reverse("spirit:admin:group:index"))
    else:
        form = GroupForm(instance=group)

    context = {'form': form, }

    return render(request, 'spirit/group/admin/update.html', context)
