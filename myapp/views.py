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
from .forms import *


def has_group(user, group_name):
    from django.contrib.auth.models import Group
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


# Create your views here.
@login_required
def index(request):
    arguments = {}
    arguments.update(csrf(request))
    if has_group(request.user, 'Клиент'):
        if request.method == "GET":
            arguments.update(form=order_client_Form)
            return render(request, 'myapp/client/index.html', {'arguments': arguments})
        elif request.method == "POST":
            new_form = order_client_Form(request.POST)
            if new_form.is_valid():
                new_form.save(user_data=request.user)
                return redirect(reverse('main_url'))
            else:
                arguments.update(error="Форма создания заказа заполнена не корректно!")
                arguments.update(form=new_form)
                return render(request, 'myapp/client/index.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    elif has_group(request.user, 'Водитель'):
        if request.method == "GET":
            arguments.update(
                order_list=order_model.objects.filter(is_delete=1, voditel_id=request.user).order_by('status_id',
                                                                                                     'time_create'))
            return render(request, 'myapp/voditel/index.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    elif has_group(request.user, 'Диспетчер'):
        if request.method == "GET":
            arguments.update(order_list=order_model.objects.filter(is_delete=1).order_by('status_id', 'time_create'))
            return render(request, 'myapp/dispatcher/index.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect(reverse('logout_url'))


@login_required
def order_list_views(request):
    arguments = {}
    if has_group(request.user, 'Клиент'):
        if request.method == "GET":
            arguments.update(order_list=order_model.objects.filter(is_delete=1, user_id=request.user).filter(
                Q(status_id=status_model.objects.get(name='В обработке')) | Q(
                    status_id=status_model.objects.get(name='Заказ принят, ожидается оплата')) | Q(
                    status_id=status_model.objects.get(name='В очереди')) | Q(
                    status_id=status_model.objects.get(name='Принят водителем/доставляется'))).order_by('-status_id'))
            return render(request, 'myapp/client/order_list.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect(reverse('main_url'))


@login_required
def order_views(request, order_id):
    arguments = {}
    if has_group(request.user, 'Клиент'):
        if request.method == "GET":
            try:
                order_object = order_model.objects.get(id=order_id, is_delete=1, user_id=request.user)
                arguments.update(order=order_object)
            except:
                arguments.update(error='Заказ не найден или принадлежит не вам!')
            return render(request, 'myapp/client/order.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    elif has_group(request.user, 'Диспетчер'):
        if request.method == "GET":
            try:
                order_object = order_model.objects.get(id=order_id, is_delete=1)
                arguments.update(order=order_object)
            except:
                arguments.update(error='Заказ не найден!')
            return render(request, 'myapp/dispatcher/order.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    elif has_group(request.user, 'Водитель'):
        if request.method == "GET":
            try:
                order_object = order_model.objects.get(id=order_id, is_delete=1, voditel_id=request.user)
                arguments.update(order=order_object)
            except:
                arguments.update(error='Заказ не найден!')
            return render(request, 'myapp/voditel/order.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect(reverse('main_url'))


@login_required
def order_edit_views(request, order_id, method):
    arguments = {}
    if has_group(request.user, 'Клиент'):
        if request.method == "GET":
            try:
                order_object = order_model.objects.get(id=order_id, is_delete=1, user_id=request.user)
                arguments.update(order=order_object)
                if method == 'pay':
                    order_object.status_id = status_model.objects.get(name='В очереди')
                    order_object.is_pay = True
                    order_object.save()
                    return redirect(reverse('order_url', args=[order_id]))
                elif method == 'cancel':
                    order_object.status_id = status_model.objects.get(name='Заказ отменен')
                    order_object.save()
                    return redirect(reverse('order_url', args=[order_id]))
            except:
                arguments.update(error='Заказ не найден или принадлежит не вам!')
            return render(request, 'myapp/client/order.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    elif has_group(request.user, 'Диспетчер'):
        if request.method == "GET":
            try:
                order_object = order_model.objects.get(id=order_id, is_delete=1)
                arguments.update(order=order_object)
                if method == 'cancel':
                    order_object.status_id = status_model.objects.get(name='Заказ отменен')
                    order_object.save()
                    return redirect(reverse('order_url', args=[order_id]))
                elif method == 'info':
                    arguments.update(form=order_dispatcher_Form)
                    return render(request, 'myapp/dispatcher/order_accept.html', {'arguments': arguments})
            except:
                arguments.update(error='Заказ не найден!')
            return render(request, 'myapp/dispatcher/order_accept.html', {'arguments': arguments})
        elif request.method == "POST":
            try:
                order_object = order_model.objects.get(id=order_id, is_delete=1)
                arguments.update(order=order_object)
                if method == 'accept':
                    new_form = order_dispatcher_Form(request.POST, instance=order_object)
                    if new_form.is_valid():
                        order_object.car_id = new_form.cleaned_data.get('car_id')
                        order_object.voditel_id = new_form.cleaned_data.get('voditel_id')
                        order_object.sum = new_form.cleaned_data.get('sum')
                        order_object.status_id = status_model.objects.get(name='В очереди')
                        order_object.save()
                        return redirect(reverse('order_url', args=[order_id]))
                    else:
                        arguments.update(error='Форма заполнена не корректно')
                        arguments.update(form=order_dispatcher_Form(request.POST))
            except:
                arguments.update(error='Заказ не найден!')
            return render(request, 'myapp/dispatcher/order_accept.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    elif has_group(request.user, 'Водитель'):
        if request.method == "GET":
            try:
                order_object = order_model.objects.get(id=order_id, is_delete=1, voditel_id=request.user)
                arguments.update(order=order_object)
                if method == 'accept':
                    order_object.status_id = status_model.objects.get(name='Заказ исполнен')
                    order_object.save()
                    return redirect(reverse('order_url', args=[order_id]))
                elif method == 'info':
                    arguments.update(form=order_voditel_Form)
                    return render(request, 'myapp/dispatcher/order_accept.html', {'arguments': arguments})
            except:
                arguments.update(error='Заказ не найден!')
            return render(request, 'myapp/dispatcher/order_accept.html', {'arguments': arguments})
        elif request.method == "POST":
            try:
                order_object = order_model.objects.get(id=order_id, is_delete=1, voditel_id=request.user)
                arguments.update(order=order_object)
                if method == 'accept':
                    new_form = order_voditel_Form(request.POST, instance=order_object)
                    if new_form.is_valid():
                        order_object.time_execution = new_form.cleaned_data.get('time_execution')
                        order_object.status_id = status_model.objects.get(name='Принят водителем/доставляется')
                        order_object.save()
                        return redirect(reverse('order_url', args=[order_id]))
                    else:
                        arguments.update(error='Форма заполнена не корректно')
                        arguments.update(form=order_voditel_Form(request.POST))
            except Exception as e:
                print(e)
                arguments.update(error='Заказ не найден!')
            return render(request, 'myapp/dispatcher/order_accept.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect(reverse('main_url'))


@login_required
def order_arhive_list_views(request):
    arguments = {}
    if has_group(request.user, 'Клиент'):
        if request.method == "GET":
            arguments.update(order_list=order_model.objects.filter(is_delete=1, user_id=request.user).filter(
                Q(status_id=status_model.objects.get(name='Заказ исполнен')) | Q(
                    status_id=status_model.objects.get(name='Заказ отменен'))).order_by('-status_id'))
            return render(request, 'myapp/client/order_list.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect(reverse('main_url'))


@login_required
def order_arhive_views(request, order_id):
    arguments = {}
    if has_group(request.user, 'Клиент'):
        if request.method == "GET":
            try:
                order_object = order_model.objects.get(id=order_id, is_delete=1, user_id=request.user)
                arguments.update(order=order_object)
            except:
                arguments.update(error='Заказ не найден или принадлежит не вам!')
            return render(request, 'myapp/client/order.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect(reverse('main_url'))


@login_required
def car_views(request):
    arguments = {}
    if has_group(request.user, 'Диспетчер'):
        if request.method == "GET":
            arguments.update(form=car_Form)
            return render(request, 'myapp/dispatcher/car_add.html', {'arguments': arguments})
        elif request.method == "POST":
            new_form = car_Form(request.POST)
            if new_form.is_valid():
                new_form.save()
                return redirect(reverse('main_url'))
            else:
                arguments.update(error="Форма добавления авто заполнена не корректно!")
                arguments.update(form=car_Form)
                return render(request, 'myapp/dispatcher/car_add.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect(reverse('main_url'))
