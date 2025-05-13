from django.db import models
import datetime
from django.contrib.auth.hashers import make_password
from django.db.models import Sum

# Categories of Products
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Customers
class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):  
        return f'{self.first_name} {self.last_name}'




# Products
class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, default=' ', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/products/')
    
    # Sales
    is_sales = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def discount_percentage(self):
        if self.is_sales and self.price > self.sale_price:
            return round(((self.price - self.sale_price) / self.price) * 100)
        return 0

    def __str__(self):
        return self.name

       

# store/models.py

class Inventory(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"



class ProductSize(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]

    product = models.ForeignKey('Products', related_name='sizes', on_delete=models.CASCADE)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES , default='S')
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'size') 

    def __str__(self):
        return f"{self.product.name} - {self.size} (Qty: {self.quantity})"


# Product Images
class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"


# Customer Orders
class Orders(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.TextField(max_length=500, default=' ', blank=True, null=True) 
    phone = models.CharField(max_length=20, default=' ', blank=True, null=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.product.name} for {self.customer.first_name}"

    class Meta:
        verbose_name_plural = "Orders"
