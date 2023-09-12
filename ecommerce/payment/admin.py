from django.contrib import admin

from .models import ShipppingAddress, Order, OrderItem

admin.site.register(ShipppingAddress)

admin.site.register(Order)

admin.site.register(OrderItem)