from django.contrib import admin
from .models import Address,Customer
# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ['user','created_at']


admin.site.register(Customer,CustomerAdmin)



class AddressAdmin(admin.ModelAdmin):
    model = Address
    list_display = ['id', 'customer','city','state','full_address','postal_code']

admin.site.register(Address, AddressAdmin)