from django.contrib import messages
from django.contrib.gis import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.admin import register, ModelAdmin
from ledger_api_client import models
from ledger_api_client import managed_models


#@admin.register(managed_models.SystemGroupPermission)
class SystemGroupPermissionInline(admin.TabularInline):
    model = managed_models.SystemGroupPermission
    extra = 0
    raw_id_fields = ('emailuser',)

    # list_display = ('id','emailuser')

@admin.register(managed_models.SystemGroup)
class SystemGroupAdmin(ModelAdmin):
    list_display = ('id','name',)
    inlines = [SystemGroupPermissionInline]

#@admin.register(models.EmailUser)
#class EmailAdmin(ModelAdmin):
#    list_display = ('id', 'first_name','last_name','is_staff','is_superuser','ledger_id',)
#    list_filter = ('is_staff','is_superuser',)
#    search_fields = ('first_name','last_name','id','ledger_id')
#
#@admin.register(models.DataStore)
#class DataStoreAdmin(ModelAdmin):
#     list_display = ('id','key_name')

