from django.contrib import admin
from .models import Products, Category, Customer, Orders, ProductImage, ProductSize ,Inventory

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Orders)
admin.site.register(ProductImage)

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 4

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductSizeInline]

class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 1
    fields = ('product', 'quantity')
admin.site.register(Products, ProductAdmin)  
admin.site.register(Inventory)

