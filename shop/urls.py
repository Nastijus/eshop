from django.urls import path
from shop import views


urlpatterns = [
    path('', views.index, name='index'),
    path('shop', views.shop, name='shop'),
    path('search', views.search, name='search'),
    path('product/<int:product_id>', views.product, name='product'),
]