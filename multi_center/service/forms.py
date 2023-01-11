from django import forms
from service.models import Extradition, Service


class ServiceForm(forms.ModelForm):
    class Meta:
        # На основе какой модели создаётся класс формы
        model = Service
        # Укажем, какие поля будут в форме
        fields = ('fio_user', 'fio_mother', 'fio_father', 'date_of_birth',
                  'serial', 'number', 'phone', 'image')


class ExtraditionForm(forms.ModelForm):
    class Meta:
        # На основе какой модели создаётся класс формы
        model = Extradition
        # Укажем, какие поля будут в форме
        fields = ('fio_user', 'fio_mother',
                  'fio_father', 'birth_certificate',
                  'phone', 'image')


class ExtraReviewForm(forms.Form):
    # На основе какой модели создаётся класс формы
    # model = Extradition
    failure = forms.CharField(
            widget=forms.Textarea,
            required=True,
            help_text='Введите причину отказа',
            error_messages={'required': ''})

