from django.contrib import admin
from .models import *
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ['id','created']


admin.site.register(Cart, CartAdmin)


class CartitemsAdmin(admin.ModelAdmin):
    model = Cartitems
    list_display = ['id','cart','product','quantity']

admin.site.register(Cartitems, CartitemsAdmin)