from django.shortcuts import render ,get_object_or_404 
from .cart import Cart
from store.models import Products
from django.http import JsonResponse
from store.models import *
import json


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()

    sub_total = sum(item['price'] * item['quantity'] for item in cart_products)

    return render(request, 'cart_summary.html', {
        'cart_products': cart_products,
        'sub_total': sub_total,
    })

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Products, id=product_id)
        size = request.POST.get('size', None)
        quantity = int(request.POST.get('quantity', 1))
        cart.add(product=product, size=size, quantity=quantity)

        cart_quantity = len(cart)
        response = JsonResponse({
            'Product Name': product.name,
            'cart_quantity': cart_quantity,
            'quantity': quantity
        })
        return response

    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

     
def cart_delete(request):
    if request.method == 'POST':
        product_id = str(request.POST.get('product_id'))
        size = request.POST.get('size')
        cart = Cart(request)

        # Identify the key for this specific item
        key = f"{product_id}_{size}" if size else product_id

        if key in cart.cart:
            del cart.cart[key]
            cart.session.modified = True

            # Save updated cart to DB if user is authenticated
            if request.user.is_authenticated:
                current_user = Profile.objects.filter(user_id=request.user.id)
                cart_json = json.dumps(cart.cart)
                current_user.update(old_cart=cart_json)

            return JsonResponse({'cart_quantity': len(cart.cart)}, status=200)

        return JsonResponse({'error': 'Item not found'}, status=404)

    return JsonResponse({'error': 'Method not allowed'}, status=405)



def cart_update(request):
    pass