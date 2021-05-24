from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _

# Create your models here.
class status_model(models.Model):
    name = models.CharField('Наименование', max_length=256, default=None)
    is_delete = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        db_table = 'status_list'

    def __str__(self):
        return self.name

class order_model(models.Model):
    name = models.CharField('Наименование', max_length=256, default=None)
    is_delete = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        db_table = 'status_list'

    def __str__(self):
        return self.name