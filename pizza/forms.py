from django import forms

from .models import Order, Pizza, Quanity

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('street', 'city', 'building_number', 'phone_number', 'comment')
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-delegate'}),
            'city': forms.TextInput(attrs={'class': 'form-delegate'}),
            'building_number': forms.NumberInput(attrs={'class': 'form-delegate'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-delegate'}),
            'comment': forms.TextInput(attrs={'class': 'form-delegate'}),
        }