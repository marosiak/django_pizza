from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import OrderForm
from .models import Order, Pizza, Quanity
from django.contrib.auth import logout
from django.utils.translation import activate

from .decorators import check_recaptcha

import requests


# Create your views here.

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('dashboard')


def orders_list(request):
    activate('pl')
    # TODO: Jakaś ładna zmiana języka
    if request.user.is_authenticated:
        orders = Order.objects.all()
        return render(request, 'pizza/orders_list.html', {'orders': orders, 'admin': True})
    else:
        orders = Order.objects.filter(tracking_key__in=request.session.get('orders', []))
        return render(request, 'pizza/orders_list.html', {'orders': orders, 'admin': False})


def order_detail(request, pk):
    activate('pl')
    order = Order.objects.get(pk=pk)
    if order.tracking_key in request.session.get('orders', []):
        return render(request, 'pizza/order_detail.html', {'order': order})
    else:
        return redirect('orders_list')


def order_deliver(request, pk):
    order = Order.objects.get(pk=pk)
    order.deliver()
    return redirect('orders_list')


def order_create(request):
    form = OrderForm()
    return render(request, 'pizza/order_create.html', {'form': form})


def dashboard(request):
    if request.user.is_authenticated:
        return redirect('orders_list')
    else:
        pizzas = Pizza.objects.all()
        return render(request, 'pizza/pizzas_list.html', {'pizzas': pizzas})


def cart_add(request, pk):
    if request.method == 'POST':
        exists = False
        for cart_item in request.session.get('cart', []):
            if cart_item['pk'] == pk:
                cart_item['count'] += 1
                exists = True
        if not exists:
            cart_item = {'pk': int(pk), 'count': 1}
            if 'cart' not in request.session:
                request.session['cart'] = [cart_item]
            else:
                request.session['cart'].append(cart_item)
        request.session.modified = True
    return redirect('dashboard')


def cart(request):
    cart_items = request.session.get('cart', [])
    total_price = 0
    for cart_item in request.session.get('cart', []):
        for pizza in Pizza.objects.all():
            if pizza.pk == cart_item['pk']:
                total_price = total_price + pizza.price * cart_item['count']
    return render(request, 'pizza/cart.html',
                  {"cart_items": cart_items, "pizzas": Pizza.objects.all(), "total_price": total_price})


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


@check_recaptcha
def order_finalize(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid() and request.recaptcha_is_valid:
            form = form.save(commit=False)
            form.start_time = timezone.now()
            import uuid
            form.tracking_key = str(uuid.uuid4())
            if 'orders' not in request.session:
                request.session['orders'] = [form.tracking_key]
            else:
                request.session['orders'].append(form.tracking_key)
            form.save()
            for item in request.session['cart']:
                pizza = Pizza.objects.get(pk=item['pk'])
                Quanity.objects.create(pizza=pizza, order=form, value=item['count'])
            form.start()
            request.session.modified = True
            return redirect('dashboard')
        else:
            form = OrderForm()
    else:
        form = OrderForm()
    return render(request, 'pizza/order_finalize.html', {'cart': request.session['cart'], 'form': form})
