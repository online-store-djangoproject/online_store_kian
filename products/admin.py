from django.contrib import admin
from .models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['id','name','discount','price','category']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['category_id','title']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)



# Register your models here.
