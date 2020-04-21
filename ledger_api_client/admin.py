from django.contrib import messages
from django.contrib.gis import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.admin import register, ModelAdmin

from ledger_api_client import models

@admin.register(models.EmailUser)
class EmailAdmin(ModelAdmin):
    list_display = ('id', 'first_name','last_name','is_staff','is_superuser','ledger_id',)
    list_filter = ('is_staff','is_superuser',)
    search_fields = ('first_name','last_name','id','ledger_id')

@admin.register(models.DataStore)
class DataStoreAdmin(ModelAdmin):
     list_display = ('id','key_name')


