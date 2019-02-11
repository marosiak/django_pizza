from django import forms

from .models import Order, Pizza, Quanity

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('street', 'city', 'building_number', 'phone_number', 'comment')