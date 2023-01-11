from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
      'pk', 'username', 'first_name',
      'last_name', 'email', 'password', 'phone')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('username',)
    empty_value_display = '-пусто-'
