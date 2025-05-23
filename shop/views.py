from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic, View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from shop.forms import ProductReviewForm, UserUpdateForm, CustomerUpdateForm
from shop.models import Category, Product, Wishlist, Customer, ProductReview, Order, OrderProduct
from django.db.models import Q


def index(request):
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories})


def shop(request):
    categories = Category.objects.all()
    query = request.GET.get('query')
    category_id = request.GET.get('category')
    products = Product.objects.all()
    if query:
        products = products.filter(Q(product_name__icontains=query))
    if category_id:
        products = products.filter(category__id=category_id)
    if request.user.is_authenticated:
        wishlist_products = request.user.customer.wishlist.values_list('product', flat=True)
    else:
        wishlist_products = []

    context = {
        'categories': categories,
        'products': products,
        'query': query if query else '',
        'wishlist_products': wishlist_products,

    }
    return render(request, 'shop.html', context=context)


class ProductDetailView(FormMixin, DetailView):
    model = Product
    template_name = 'product.html'
    form_class = ProductReviewForm

    def get_success_url(self):
        return reverse('product', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if form.cleaned_data['rating'] is None:
            form.add_error('rating', 'Rating is required!')
            return self.form_invalid(form)

        customer = Customer.objects.get(user=self.request.user)
        product = self.object

        is_existing_review = ProductReview.objects.filter(customer=customer, product=product).first()
        if is_existing_review:
            is_existing_review.rating = form.cleaned_data['rating']
            is_existing_review.content = form.cleaned_data['content']
            is_existing_review.save()
        else:
            form.instance.product = product
            form.instance.customer = customer
            form.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            wishlist_products = self.request.user.customer.wishlist.values_list('product', flat=True)
            wishlist_count = self.request.user.customer.wishlist.count()
        else:
            wishlist_products = []
            wishlist_count = 0

        context['wishlist_products'] = wishlist_products
        context['wishlist_count'] = wishlist_count
        context['stars'] = [5,4,3,2,1]

        return context


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


@login_required
def customer_profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        customer_form = CustomerUpdateForm(request.POST, instance=request.user.customer)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            messages.success(request, f"Profile updated")
            return redirect('customer_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        customer_form = CustomerUpdateForm(instance=request.user.customer)

    context = {
        'user_form': user_form,
        'customer_form': customer_form,
    }
    return render(request, 'customer_profile.html', context)


class WishlistByUserListView(LoginRequiredMixin, generic.ListView):
    model = Wishlist
    template_name = 'my_wishlist.html'
    paginate_by = 10

    def get_queryset(self):
        return Wishlist.objects.filter(customer__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            wishlist_products = self.request.user.customer.wishlist.values_list('product', flat=True)
            wishlist_categories = Category.objects.filter(
                products__wishlist__customer__user=self.request.user).distinct()
        else:
            wishlist_products = []
            wishlist_categories = []

        context['wishlist_products'] = wishlist_products
        context['wishlist_categories'] = wishlist_categories

        return context


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = request.user.customer

    wishlist_item, created = Wishlist.objects.get_or_create(customer=customer, product=product)
    if not created:
        wishlist_item.delete()
        messages.info(request, 'Product removed from wishlist.')
    else:
        messages.success(request, 'Product added to wishlist.')
    return redirect(request.META.get('HTTP_REFERER', 'shop'))


class AddToCartView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        product = Product.objects.filter(id=product_id).first()
        if not product:
            return redirect('index')

        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            order, created = Order.objects.get_or_create(customer=customer, status='cart')
            order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)
            if created:
                order_product.quantity = quantity
            else:
                order_product.quantity += quantity
            order_product.save()
        else:
            cart = request.session.get('cart', {})
            cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
            request.session['cart'] = cart

        return redirect(request.META.get('HTTP_REFERER', 'shop'))


class UpdateCartView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        cart_open = request.POST.get('cart_open')

        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            order = Order.objects.get(customer=customer, status='cart')
            product = OrderProduct.objects.filter(order=order, product_id=product_id).first()

            if product:
                if action == 'plus':
                    product.quantity += 1
                    product.save()
                elif action == 'minus':
                    product.quantity -= 1
                    product.save()
                    if product.quantity <= 0:
                        product.delete()
        else:
            cart = request.session.get('cart', {})
            if product_id in cart:
                if action == 'plus':
                    cart[product_id] += 1
                elif action == 'minus':
                    cart[product_id] -= 1
                    if cart[product_id] <= 0:
                        del cart[product_id]
            request.session['cart'] = cart

        redirect_url = '/'
        if cart_open:
            redirect_url += '?cart_open=1'

        return redirect(redirect_url)


class CheckoutView(TemplateView):
    template_name = 'checkout.html'

    def post(self, request):
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('index')

        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
        else:
            customer = Customer.objects.create(user=None)

        order = Order.objects.create(customer=customer, status='payment')
        products = Product.objects.filter(id__in=cart.keys())

        for product in products:
            quantity = cart.get(str(product.id), 1)
            OrderProduct.objects.create(order=order, product=product, quantity=quantity)

        request.session['cart'] = {}
        return redirect('order_success', order_id=order.id)
