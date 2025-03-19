from django.contrib import admin
from .models import Address
# Register your models here.

class AddressAdmin(admin.ModelAdmin):
    model = Address
    list_display = ['id', 'user','city','state','full_address','postal_code']

admin.site.register(Address, AddressAdmin)