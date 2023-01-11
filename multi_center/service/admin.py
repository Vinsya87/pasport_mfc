from django.contrib import admin

from .models import Extradition, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'pub_date', 'author', 'review')
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Extradition)
class ExtraditionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'pub_date', 'author', 'review')
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
