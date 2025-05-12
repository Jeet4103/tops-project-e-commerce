from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Products , ProductImage
from .forms import SignUpForm
from .forms import MultipleImageUploadForm

# Homepage view
def home(request):
    products = Products.objects.all()
    return render(request, 'home.html', {'products': products})

def cart(request):
    return render(request, 'cart.html')

def about(request):
    return render(request, 'about.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username") 
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)  

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect('home')  
        else:
            messages.error(request, "Invalid username or password")  # Fixed
            return redirect('login')  # Redirect instead of render to avoid resubmission

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

def product_detail(request,pk):
    product = Products.objects.get(id = pk)
    images = ProductImage.objects.filter(product=product)
    
    return render(request, 'product_detail.html', {'product': product, 'images': images})


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


