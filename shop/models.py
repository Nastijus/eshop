from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    logo = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    description = models.TextField(max_length=1000, default='', blank=True, null=True)
    image = models.ImageField(upload_to='products', null=True)

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path).convert("RGBA")
        img_width, img_height = img.size
        max_size = max(img_width, img_height)
        img_alfa = Image.new("RGBA", (max_size, max_size), (0, 0, 0, 0))
        x = (max_size - img_width) // 2
        y = (max_size - img_height) // 2
        img_location = (x, y)
        img_alfa.paste(img, img_location)
        img_alfa.save(self.image.path, format="PNG")


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('customer', 'product')


class ProductReview(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    description = models.TextField(max_length=1000, default='', blank=True, null=True)

    class Meta:
        unique_together = ('customer', 'product')


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date = models.DateField(default=timezone.now)

    LOAN_STATUS = (
        ('cart', 'Shopping Cart'),
        ('payment', 'Awaiting Payment'),
        ('shipping', 'Awaiting Shipment'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )

    status = models.CharField(
        choices=LOAN_STATUS,
        blank=True,
        default='card',
        help_text='Status',
    )

    def __str__(self):
        return str(self.date)
