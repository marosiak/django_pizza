from django.shortcuts import render, redirect
from django.core import serializers
from django.utils import timezone

from .models import Order, Pizza, Quanity
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
        count = int(request.POST['count'])
        exists = False
        for cart_item in request.session.get('cart', []):
            if cart_item['pk'] == pk:
                cart_item['count'] += count
                exists = True
        if not exists:
            cart_item = {'pk': int(pk), 'count': count}
            if 'cart' not in request.session:
                request.session['cart'] = [cart_item]
            else:
                request.session['cart'].append(cart_item)
        request.session.modified = True
    return redirect('pizzas_list')


def cart(request):
    cart_items = request.session.get('cart', [])
    total_price = 0
    for cart_item in request.session['cart']:
        for pizza in Pizza.objects.all():
            if pizza.pk == cart_item['pk']:
                total_price = total_price+pizza.price*cart_item['count']
    return render(request, 'pizza/cart.html', {"cart_items": cart_items, "pizzas": Pizza.objects.all(), "total_price": total_price})

def cart_remove_item(request, pk):
    request.session['cart'].pop(pk)
    request.session.modified = True
    return redirect('cart')


def cart_clear(request):
    request.session['cart'] = []
    return redirect('cart')


def cart_update(request, pk):
    if request.method == 'POST':
        count = int(request.POST['count'])
        for cart_item in request.session['cart']:
            if cart_item['pk'] == pk:
                if count > 0:
                    cart_item['count'] = count
                    request.session.modified = True
    return redirect('cart')


def order_finalize(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.start_time = timezone.now()
            form.save()
            for item in request.session['cart']:
                pizza = Pizza.objects.get(pk=item['pk'])
                Quanity.objects.create(pizza=pizza, order=form, value=item['count'])
            return redirect('pizzas_list')
        else:
            form = OrderForm()
    else:
        form = OrderForm()
    return render(request, 'pizza/order_finalize.html', {'cart': request.session['cart'], 'form': form })