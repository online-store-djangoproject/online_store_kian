from django.contrib import admin
from .models import Address, DiscountCode
# Register your models here.

class AddressAdmin(admin.ModelAdmin):
    model = Address
    list_display = ['id', 'user','city','state','full_address','postal_code']

admin.site.register(Address, AddressAdmin)


class DiscountCodeAdmin(admin.ModelAdmin):
    model = DiscountCode
    list_display = ['id', 'user','code','percentage','created_at']

admin.site.register(DiscountCode, DiscountCodeAdmin)