from django.contrib.auth import user_logged_in
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from shop.models import Customer, Order, Product, OrderProduct


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
        print('KWARGS: ', kwargs)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.customer.save()


@receiver(user_logged_in)
def merge_session_to_database(sender, request, user, **kwargs):
    cart = request.session.get('cart', {})
    if not cart:
        return

    customer = Customer.objects.get(user=user)
    order, created = Order.objects.get_or_create(customer=customer, status='cart')

    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id).first()
        if product:
            order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)
            if not created:
                order_product.quantity += quantity
            else:
                order_product.quantity = quantity
            order_product.save()

    del request.session['cart']
    request.session.modified = True
