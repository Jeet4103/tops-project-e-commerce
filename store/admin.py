# store/admin.py
from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Orders)
admin.site.register(ProductImage)
admin.site.register(Profile)


class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username','first_name','last_name','email']
    inline = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

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
