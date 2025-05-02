from datetime import datetime
from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='logo', null=True)

    def __str__(self):
        return self.category_name

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.DecimalField
    caregory = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, default='', blank=True, null=True)
    image = models.ImageField(upload_to='products', null=True)

    def __str__(self):
        return self.product_name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date = models.DateField(default=datetime.today())

    def __str__(self):
        return str(self.date)
