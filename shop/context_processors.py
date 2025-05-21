import random

from shop.models import Customer, Order, OrderProduct, Product


def wishlist_context(request):
    if request.user.is_authenticated:
        wishlist_count = request.user.customer.wishlist.count()
    else:
        wishlist_count = 0

    return {
        'wishlist_count': wishlist_count,
    }

def cart_context(request):
    cart_open = request.GET.get('cart_open') == '1'
    cart_products = []
    total = 0
    count = 0

    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, status='cart')
        products = OrderProduct.objects.filter(order=order).select_related('product')

        for product in products:
            subtotal = product.product.price * product.quantity
            total += subtotal
            count += product.quantity
            cart_products.append({
                'product': product.product,
                'quantity': product.quantity,
                'subtotal': subtotal
                })

    else:
        cart = request.session.get('cart', {})
        product_ids = list(cart.keys())
        products = Product.objects.filter(id__in=product_ids)
        product_dict = {str(p.id): p for p in products}

        for product_id, quantity in cart.items():
            product = product_dict.get(str(product_id))
            if product:
                subtotal = product.price * quantity
                total += subtotal
                count += quantity
                cart_products.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': subtotal
                })

    return {
        'cart_open': cart_open,
        'cart_products': cart_products,
        'cart_total': total,
        'cart_count': count
    }

def random_products(request):
    all_products = list(Product.objects.all())
    random_products = random.sample(all_products, min(6, len(all_products)))
    return {'random_products': random_products}