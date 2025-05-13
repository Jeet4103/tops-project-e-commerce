# store/admin.py
from django.contrib import admin
from .models import Products, Category, Customer, Orders, ProductImage, ProductSize, Inventory

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Orders)
admin.site.register(ProductImage)

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_inventory_quantity')
    inlines = [ProductSizeInline]  
    
    def get_inventory_quantity(self, obj):
        inventory = Inventory.objects.filter(product=obj).first()
        return inventory.quantity if inventory else 0
    

    get_inventory_quantity.short_description = 'Inventory Qty'

admin.site.register(Products, ProductAdmin)
