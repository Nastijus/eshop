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
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')