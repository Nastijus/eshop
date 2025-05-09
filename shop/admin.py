from django.contrib import admin

from .models import Category, Customer, Product, Order, Wishlist, ProductReview

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Wishlist)
admin.site.register(ProductReview)
admin.site.register(Order)