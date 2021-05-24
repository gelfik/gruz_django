from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.utils import timezone
from .models import *
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def has_group(user, group_name):
    from django.contrib.auth.models import Group
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

# Create your views here.

@login_required
def index(request):
    arguments = {}
    arguments.update(csrf(request))
    if request.method == "GET":
        if has_group(request.user, 'Сотрудник'):
            return redirect(reverse('sotr_tasklist_url'))
        elif has_group(request.user, 'Руководитель'):
            return redirect(reverse('worklist_url'))
        else:
            auth.logout(request)
            return redirect('/')
    else:
        return HttpResponse('405 Method Not Allowed', status=405)