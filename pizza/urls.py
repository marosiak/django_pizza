from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.orders_list, name='orders_list'),
    path('', views.pizzas_list, name='pizzas_list'),

    path('order/<int:pk>', views.order_detail, name='order_detail'),
    path('order_deliver/<int:pk>', views.order_deliver, name='order_deliver'),
    path('order/create/', views.order_create, name='order_create'),

    path('pizza/<int:pk>', views.cart_add, name='cart_add'),

    path('cart', views.cart, name='cart'),
    path('cart/clear', views.cart_clear, name='cart_clear')

]