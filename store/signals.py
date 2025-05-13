# store/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProductSize, Inventory
from django.db.models import Sum

def update_inventory_quantity(product):
    total_quantity = ProductSize.objects.filter(product=product).aggregate(total=Sum('quantity'))['total'] or 0
    Inventory.objects.update_or_create(product=product, defaults={'quantity': total_quantity})

@receiver(post_save, sender=ProductSize)
def update_inventory_on_save(sender, instance, **kwargs):
    update_inventory_quantity(instance.product)

@receiver(post_delete, sender=ProductSize)
def update_inventory_on_delete(sender, instance, **kwargs):
    update_inventory_quantity(instance.product)
