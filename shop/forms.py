from django.contrib.auth.models import User

from .models import ProductReview, Customer
from django import forms

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ('content', 'product', 'customer', 'rating')
        widgets = {
            'product': forms.HiddenInput(),
            'customer': forms.HiddenInput(),
            'rating': forms.RadioSelect(choices=[(i, f"{i} ⭐") for i in range(1, 6)])
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone', 'address']