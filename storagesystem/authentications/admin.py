from django.contrib import admin
from . models import *

# Register your models here.

class StaffNumberAdmin(admin.ModelAdmin):
    list_display = ['number', 'is_in_use']

admin.site.register(StaffNumber, StaffNumberAdmin)
admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(storageProvider)
admin.site.register(Profile)



