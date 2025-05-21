from django.contrib import admin

from .models import Category, Customer, Product, Order, Wishlist, ProductReview, OrderProduct

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'logo')
    inlines = [ProductInline]

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'category', 'description', 'image')
    search_fields = ('product_name', 'description')

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date', 'status')
    inlines = [OrderProductInline]

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product')

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'rating', 'content', 'date_created')

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
