from itertools import product

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
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