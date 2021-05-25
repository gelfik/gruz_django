from django.contrib import admin
from .models import *


@admin.register(status_model)
class status_list(admin.ModelAdmin):
    list_display = ('name', 'id','is_delete')

@admin.register(measure_size_model)
class measure_size_list(admin.ModelAdmin):
    list_display = ('name', 'full_name', 'is_delete')

@admin.register(measure_ves_model)
class measure_ves_list(admin.ModelAdmin):
    list_display = ('name', 'full_name', 'is_delete')

@admin.register(gruz_type_model)
class gruz_type_list(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_delete')


@admin.register(car_model)
class car_list(admin.ModelAdmin):
    list_display = ('marka', 'gos_number', 'is_delete')

@admin.register(order_model)
class order_list(admin.ModelAdmin):
    list_display = ('gruz_type_id', 'status_id', 'lenght', 'height', 'width', 'ves', 'is_pay', 'time_create', 'time_execution', 'sum', 'car_id', 'voditel_id')