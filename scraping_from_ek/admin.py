from django.contrib import admin

from scraping_from_ek.models import *


admin.site.register(Component)
admin.site.register(Manufacturer)


@admin.register(Gpu)
class GpuAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'wed_price', 'manufacturer')
    list_filter = ('model', 'manufacturer')


@admin.register(Cpu)
class CpuAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'wed_price', 'manufacturer')
    list_filter = ('model', 'manufacturer')


@admin.register(Url)
class CpuAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'url')
    list_filter = ('manufacturer', 'model')


@admin.register(Errors)
class CpuAdmin(admin.ModelAdmin):
    list_display = ('time', 'data')





