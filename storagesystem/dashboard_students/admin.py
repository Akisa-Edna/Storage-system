from django.contrib import admin
from . models import *

# Register your models here.
#admin.site.register(Student)
admin.site.register(Container)
admin.site.register(Category)
admin.site.register(Booking)
admin.site.register(Contact)
#admin.site.register(StorageProvider)

'''class LNMOnlineAdmin(admin.ModelAdmin):
    list_display = ("PhoneNumber", "Amount", "MpesaReceiptNumber", "TransactionDate")

admin.site.register(LNMOnline,LNMOnlineAdmin)

'''
