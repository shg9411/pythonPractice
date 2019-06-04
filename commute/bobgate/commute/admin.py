from django.contrib import admin
from .models import Employee, Department, Work


@admin.register(Employee)
class EmplyeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'department']
    list_display_links = ['name', 'department']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['department']


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ['name']