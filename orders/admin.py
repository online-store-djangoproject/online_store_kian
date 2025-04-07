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


# Order  OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity')
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'pending_status', 'placed_at')
    list_filter = ('pending_status', 'placed_at')
    search_fields = ('id', 'owner__email', 'owner__username')
    readonly_fields = ('placed_at',)
    inlines = [OrderItemInline]

    fieldsets = (
        ('اطلاعات سفارش', {
            'fields': ('owner', 'pending_status', 'placed_at')
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__id', 'product__title')
    list_filter = ('product',)