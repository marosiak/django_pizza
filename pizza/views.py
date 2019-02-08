from django.shortcuts import render, redirect
from django.core import serializers
from .models import Order
from django.http import JsonResponse
# Create your views here.

def orders_list(request):
    orders = Order.objects.all()
    return render(request, 'pizza/orders_list.html', {'orders': orders})

def order_detail(request, pk):
    orders = Order.objects.get(pk=pk)
    # import ipdb; ipdb.set_trace()
    return render(request, 'pizza/order_detail.html', {'order': orders})

def order_deliver(request, pk):
    order = Order.objects.get(pk=pk)
    order.deliver()
    return redirect('orders_list')