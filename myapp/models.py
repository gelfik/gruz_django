from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _


# Create your models here.
class status_model(models.Model):
    name = models.CharField('Наименование', max_length=256, default=None)
    is_delete = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'
        db_table = 'status_model'

    def __str__(self):
        return self.name


class measure_size_model(models.Model):
    name = models.CharField('Сокращение', max_length=256, default=None)
    full_name = models.CharField('Полное наименование', max_length=256, default=None)
    is_delete = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Еденица измерения размера'
        verbose_name_plural = 'Еденицы измерения размера'
        db_table = 'measure_size'

    def __str__(self):
        return self.name


class measure_ves_model(models.Model):
    name = models.CharField('Сокращение', max_length=256, default=None)
    full_name = models.CharField('Полное наименование', max_length=256, default=None)
    is_delete = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Еденица измерения веса'
        verbose_name_plural = 'Еденицы измерения веса'
        db_table = 'measure_ves'

    def __str__(self):
        return self.name


class gruz_type_model(models.Model):
    name = models.CharField('Наименование', max_length=256, default=None)
    description = models.TextField('Описание', default=None)
    is_delete = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Тип груза'
        verbose_name_plural = 'Типы груза'
        db_table = 'gruz_type_model'

    def __str__(self):
        return self.name


class car_model(models.Model):
    marka = models.CharField('Марка ТС', max_length=256, default=None)
    gos_number = models.CharField('Государственный номер', max_length=256, default=None)
    is_delete = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Автотраспорт'
        verbose_name_plural = 'Автотраспорты'
        db_table = 'car_model'

    def __str__(self):
        return self.gos_number


class order_model(models.Model):
    user_id = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE, verbose_name='Клиент',
                                default=None)
    status_id = models.ForeignKey(status_model, on_delete=models.CASCADE, verbose_name='Статус заказа', default=None)
    gruz_type_id = models.ForeignKey(gruz_type_model, on_delete=models.CASCADE, verbose_name='Тип груза', default=None)
    lenght = models.FloatField('Длина груза', default=0)
    height = models.FloatField('Высота груза', default=0)
    width = models.FloatField('Ширина груза', default=0)
    ves = models.FloatField('Вес груза', default=0)
    measure_size_id = models.ForeignKey(measure_size_model, on_delete=models.CASCADE,
                                        verbose_name='Еденица измерения размера', default=None)
    measure_ves_id = models.ForeignKey(measure_ves_model, on_delete=models.CASCADE,
                                       verbose_name='Еденица измерения веса', default=None)
    start_point = models.CharField('Начальный пункт', max_length=256, default=None)
    finish_point = models.CharField('Конечный пункт', max_length=256, default=None)
    is_pay = models.BooleanField('Статус оплаты', default=False)
    time_create = models.DateTimeField('Время заявки', auto_now_add=True)
    time_execution = models.DateTimeField('Время исполнения заявки', default=None, null=True, blank=True)
    sum = models.FloatField('Стоимость', default=0, blank=True)
    car_id = models.ForeignKey(car_model, on_delete=models.CASCADE, verbose_name='Машина', default=None, null=True,
                               blank=True)
    voditel_id = models.ForeignKey(User, related_name='voditels', on_delete=models.CASCADE, verbose_name='Водитель',
                                   default=None, null=True, blank=True)
    is_delete = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        db_table = 'order_model'

    def __str__(self):
        return str(self.time_create)
