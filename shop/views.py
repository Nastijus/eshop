from itertools import product

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from shop.models import Category, Product
from django.db.models import Q
from django.shortcuts import render, get_object_or_404


def index(request):
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories})


def shop(request):
    categories = Category.objects.all()
    query = request.GET.get('query')
    if query:
        products = Product.objects.filter(Q(product_name__icontains=query))
    else:
        products = Product.objects.all()

    context = {
        'categories': categories,
        'products': products,
        'query': query,
    }
    return render(request, 'shop.html', context=context)


def search(request):
    query = request.GET.get('query')
    return HttpResponseRedirect(f"{reverse('shop')}?query={query}")


def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product.html', {'product': product})


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} is already taken!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'A user with email {email} is already registered!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'User {username} has been registered!')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    return render(request, 'register.html')
