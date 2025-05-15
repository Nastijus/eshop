from django.urls import path
from shop import views


urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product'),
    path('register/', views.register, name='register'),
    path('mywishlist/', views.WishlistByUserListView.as_view(), name='my-wishlist'),
    path('customer_profile/', views.customer_profile, name='customer_profile'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
]