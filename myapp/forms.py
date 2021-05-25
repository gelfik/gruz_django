from django import forms
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext, gettext_lazy as _
from django.forms import ModelForm
from .models import *


class UserFullName(User):
    class Meta:
        proxy = True
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return self.get_full_name()


class car_FullName(car_model):
    class Meta:
        proxy = True
        ordering = ["marka"]

    def __str__(self):
        return f'{self.marka} - {self.gos_number}'


class measure_size_FullName(measure_size_model):
    class Meta:
        proxy = True
        ordering = ["name"]

    def __str__(self):
        return f'{self.name} - {self.full_name}'


class measure_ves_FullName(measure_ves_model):
    class Meta:
        proxy = True
        ordering = ["name"]

    def __str__(self):
        return f'{self.name} - {self.full_name}'


class car_Form(ModelForm):
    marka = forms.CharField(label=_("Марка ТС"), widget=forms.TextInput(attrs={'class': 'form-control'}))
    gos_number = forms.CharField(label=_("Государственный номер"),
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = car_model
        fields = ['marka', 'gos_number']


class order_client_Form(ModelForm):
    user_id = forms.ModelChoiceField(label=_("Клиент"), widget=forms.Select(attrs={'class': 'form-control'}),
                                     queryset=None)
    gruz_type_id = forms.ModelChoiceField(label=_("Тип груза"), widget=forms.Select(attrs={'class': 'form-control'}),
                                          queryset=None)
    lenght = forms.FloatField(label=_("Длина груза"), widget=forms.NumberInput(attrs={'class': 'form-control'}))
    height = forms.FloatField(label=_("Высота груза"), widget=forms.NumberInput(attrs={'class': 'form-control'}))
    width = forms.FloatField(label=_("Ширина груза"), widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ves = forms.FloatField(label=_("Вес груза"), widget=forms.NumberInput(attrs={'class': 'form-control'}))
    measure_size_id = forms.ModelChoiceField(label=_("Еденица измерения размера"),
                                             widget=forms.Select(attrs={'class': 'form-control'}),
                                             queryset=None)
    measure_ves_id = forms.ModelChoiceField(label=_("Еденица измерения веса"),
                                            widget=forms.Select(attrs={'class': 'form-control'}),
                                            queryset=None)
    start_point = forms.CharField(label=_("Начальный пункт"), widget=forms.TextInput(attrs={'class': 'form-control'}))
    finish_point = forms.CharField(label=_("Конечный пункт"), widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = order_model
        fields = ['gruz_type_id', 'lenght', 'height', 'width', 'ves', 'measure_size_id', 'measure_ves_id',
                  'start_point', 'finish_point']

    def __init__(self, *args, **kwargs):
        super(order_client_Form, self).__init__(*args, **kwargs)
        # self.fields['user_id'].queryset = User.objects.filter(is_active=1)
        self.fields['gruz_type_id'].queryset = gruz_type_model.objects.filter(is_delete=1)
        self.fields['measure_size_id'].queryset = measure_size_FullName.objects.filter(is_delete=1)
        self.fields['measure_ves_id'].queryset = measure_ves_FullName.objects.filter(is_delete=1)
        del self.fields['user_id']

    def save(self, commit=True, user_data=None):
        data = super(order_client_Form, self).save(commit=False)
        data.user_id = user_data
        if self.instance and self.instance.pk is None:
            data.status_id = status_model.objects.get(name='В обработке')
            data.car_id = None
        if commit:
            data.save()
        return data


class order_dispatcher_Form(ModelForm):
    sum = forms.CharField(label=_("Стоимость"), widget=forms.NumberInput(attrs={'class': 'form-control'}))
    car_id = forms.ModelChoiceField(label=_("Машина"), widget=forms.Select(attrs={'class': 'form-control'}),
                                    queryset=None)
    voditel_id = forms.ModelChoiceField(label=_("Водитель"), widget=forms.Select(attrs={'class': 'form-control'}),
                                        queryset=None)

    class Meta:
        model = order_model
        fields = ['sum', 'car_id', 'voditel_id']

    def __init__(self, *args, **kwargs):
        super(order_dispatcher_Form, self).__init__(*args, **kwargs)
        self.fields['car_id'].queryset = car_FullName.objects.filter(is_delete=1)
        self.fields['voditel_id'].queryset = UserFullName.objects.filter(groups__name='Водитель')


class order_voditel_Form(ModelForm):
    time_execution = forms.DateTimeField(label=_("Расчетное время исполнения заявки"), widget=forms.DateTimeInput(
        attrs={'class': 'form-control', 'type': 'datetime-local'}))

    class Meta:
        model = order_model
        fields = ['time_execution']
