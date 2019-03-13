from django.conf import settings
from django.db import models as models
from django.urls import reverse
from django.utils import timezone


class Order(models.Model):
    # Fields
    street = models.CharField(max_length=25)
    city = models.CharField(max_length=30)
    building_number = models.IntegerField()
    start_time = models.DateTimeField(editable=False, blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True, auto_now=False, editable=False)
    phone_number = models.CharField(max_length=12)
    comment = models.TextField(max_length=150, blank=True)

    total_price = models.IntegerField(blank=True, null=True, editable=False)
    # TODO: Obliczanie total_price
    start_time = timezone.now()

    # Relationship Fields
    pizzas = models.ManyToManyField(
        'Pizza',
        related_name="orders",
        through="Quanity"
    )

    def deliver(self):
        self.end_time = timezone.now()
        self.save()

    def __str__(self):
        return self.street + ", " + self.phone_number


class Pizza(models.Model):
    # Fields
    name = models.CharField(max_length=255)
    price = models.IntegerField()

    # Relationship Fields
    ingradients = models.ManyToManyField(
        'Ingradient',
        related_name="pizzas"
    )

    def __str__(self):
        return self.name


class Ingradient(models.Model):
    # Fields
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Quanity(models.Model):
    pizza = models.ForeignKey("Pizza", verbose_name="Pizza", on_delete=models.CASCADE, related_name="quanities")
    order = models.ForeignKey("Order", verbose_name="Zamówienie", on_delete=models.CASCADE)

    value = models.IntegerField("Ilosc", default=1)

    def __str__(self):
        return self.pizza.name + ": " + str(self.value)
