from django.contrib import admin

from .models import Order, Pizza, Ingradient, Quanity

admin.site.register(Pizza)
admin.site.register(Order)
admin.site.register(Ingradient)
admin.site.register(Quanity)

# Register your models here.
