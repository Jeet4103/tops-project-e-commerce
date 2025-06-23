from django.shortcuts import render, redirect  
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Products, ProductImage, Category
from .forms import *
import re
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
import json
from cart.cart import Cart

# Homepage view
def home(request):
    products = Products.objects.all()
    categories = Category.objects.all()

    return render(request, 'home.html', {'products': products, 'categories': categories})
 
def about(request):
    return render(request, 'about.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username") 
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password) 
        if user is not None:
            login(request, user)

            # Get user saved cart
            current_user = Profile.objects.get(user_id=user.id)
            saved_cart = current_user.old_cart

            cart = Cart(request)
            if saved_cart:
                cart.merge_old_cart(saved_cart)

            # IMPORTANT: Save merged cart back to DB & session
            cart.save()

            messages.success(request, "You have been logged in.")
            return redirect('home')  
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def SignUp(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save() 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']  
            user = authenticate(username=username, password=password)
            if user is not None: 
                login(request, user)
                messages.success(request, "You have Registered Successfully.")
                return redirect('home')
            else:
                messages.error(request, "Authentication failed. Please try logging in.")
        else:
            messages.error(request, "Sorry, there was a problem signing up. Please try again.")

    return render(request, 'signup.html', {'form': form})

def Profile_update(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_instance = Profile.objects.get(user=current_user)

        user_form = Profile_updateform(request.POST or None, instance=current_user)
        user_info = Profile_infoform(request.POST or None, instance=profile_instance)

        if user_form.is_valid() and user_info.is_valid():
            user_form.save()
            user_info.save()
            login(request, current_user)
            messages.success(request, 'User has been updated')
            return redirect('home')

        products = Products.objects.all()
        categories = Category.objects.all()
        return render(request, 'Profile_update.html', {
            'user_form': user_form,
            'user_info': user_info,
            'products': products,
            'categories': categories,
            'user': current_user
        })


def Password_update(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        form = Password_updateForm(user, request.POST if request.method == "POST" else None)
        if request.method == "POST":
            if form.is_valid():
                old_password = form.cleaned_data.get('old_password')
                new_password1 = form.cleaned_data.get('new_password1')
                new_password2 = form.cleaned_data.get('new_password2')
                if user.check_password(old_password):
                    if new_password1 == new_password2:
                        user.set_password(new_password1)
                        user.save()
                        update_session_auth_hash(request, user)
                        messages.success(request, 'Password updated successfully')
                        return redirect('home')
                    else:
                        messages.error(request, 'New passwords do not match')
                else:
                    messages.error(request, 'Old password is incorrect')
        return render(request, 'Password_update.html', {'form': form})
    else:       
        return redirect('login' )

def product_detail(request, pk):
    product = get_object_or_404(Products, id=pk)            
    images = ProductImage.objects.filter(product=product)
    categories = Category.objects.all()
    available_sizes = list(
        product.sizes.filter(quantity__gt=0).values_list('size', flat=True)
    )

    all_sizes = ['S', 'M', 'L', 'XL']
    context = {
        'product': product,
        'images': images,
        'categories': categories,
        'available_sizes': available_sizes,
        'all_sizes': all_sizes,
    }
    return render(request, 'product_detail.html', context)

def upload_product_images(request):
    if request.method == 'POST':
        form = MultipleImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.cleaned_data['product']
            files = request.FILES.getlist('images')

            for file in files:
                ProductImage.objects.create(product=product, image=file)

            return redirect('product_detail', pk=product.id)

    else:
        form = MultipleImageUploadForm()
    
    return render(request, 'upload_images.html', {'form': form})

def normalize_string(s):
    # Convert to lowercase
    s = s.replace('-', ' ')
    s = re.sub(r"[^\w\s]", '', s)
    return s.lower().strip()

def category(request, category_name):
    normalized_input = normalize_string(category_name)
    matched_category = None
    for cat in Category.objects.all():
        if normalize_string(cat.name) == normalized_input:
            matched_category = cat
            break

    if matched_category:
        products = Products.objects.filter(category=matched_category)
        categories = Category.objects.all()
        return render(request, 'category.html', { 'category': matched_category, 'products': products, 'categories': categories })
    else:
        messages.error(request, "Category not found.")
        return redirect('home')

    
   



