from django.shortcuts import render
from shop.models import Category, Product


def index(request):
    categories = Category.objects.all()
    # products = Product.objects.all()


    context = {
        'categories':categories,
        # 'products': products,
      }

    return render(request, 'index.html', context=context)

def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()


    context = {
        'categories':categories,
        'products': products,
      }

    return render(request, 'shop.html', context=context)