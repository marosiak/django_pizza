from django.shortcuts import render, redirect
from django.core import serializers
from .models import Order, Pizza
from .forms import OrderForm
import ipdb
import json


# Create your views here.

def orders_list(request):
    orders = Order.objects.all()
    return render(request, 'pizza/orders_list.html', {'orders': orders})


def order_detail(request, pk):
    orders = Order.objects.get(pk=pk)
    return render(request, 'pizza/order_detail.html', {'order': orders})


def order_deliver(request, pk):
    order = Order.objects.get(pk=pk)
    order.deliver()
    return redirect('orders_list')


def order_create(request):
    form = OrderForm()
    return render(request, 'pizza/order_create.html', {'form': form})


def pizzas_list(request):
    pizzas = Pizza.objects.all()
    return render(request, 'pizza/pizzas_list.html', {'pizzas': pizzas})


def cart_add(request, pk):
    if request.method == 'POST':
        request.session.get('cart', [])
        cart_item = {'pk': int(pk), 'count': int(request.POST['count'])}
        request.session['cart'].append(cart_item)
        request.session.modified = True
    return redirect('pizzas_list')


def cart(request):
    cart_items = request.session.get('cart', [])
    return render(request, 'pizza/cart.html', {"cart_items": cart_items, "pizzas": Pizza.objects.all()})


def cart_remove_item(request, index):
    # data = request.session['cart']
    # data.pop(index)
    # request.session['cart'] = data
    request.session['cart'].pop(index)
    request.session.modified = True
    return redirect('cart')


def cart_clear(request):
    request.session.get('cart', [])  # in case this object doesnt exists
    request.session['cart'] = []
    return redirect('cart')
