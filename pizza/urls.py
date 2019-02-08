from django.urls import path
from . import views

urlpatterns = [
    path('', views.orders_list, name='orders_list'),
    path('order/<int:pk>', views.order_detail, name='order_detail'),
    path('order_deliver/<int:pk>', views.order_deliver, name='order_deliver'),

]