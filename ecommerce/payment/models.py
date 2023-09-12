from django.db import models

from django.contrib.auth.models import User

from store.models import Product

class ShipppingAddress(models.Model):

    full_name = models.CharField(max_length=300)

    email = models.EmailField(max_length=255)

    address1 = models.CharField(max_length=300)

    address2 = models.CharField(max_length=300)

    city = models.CharField(max_length=255)
 
    # null = True and blank = True is an optional FIELD
    state = models.CharField(max_length=255, null=True, blank=True)

    zipcode = models.CharField(max_length=255, null=True, blank=True)

    # Foreign Key
    # If that user delete their account, then this shippaddress info will also be deleted

    # Authenticated / not authenticated users
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Change the name in the admin
    class Meta:

        verbose_name_plural = 'Shipping Address'

    
    def __str__(self):

        return 'Shipping Address - ' + str(self.id)
    
class Order(models.Model):

    full_name = models.CharField(max_length=300)

    email = models.EmailField(max_length=255)

    shipping_address = models.TextField(max_length=1000)

    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)

    date_ordered = models.DateTimeField(auto_now_add=True)

    # Foreign Key

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):

        return 'Order - #' + str(self.id)
    
class OrderItem(models.Model):

    # If the Order is deleted, then the orderItem is gone toom
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)

    # If the Product got deleted, then it makes no sense to order the item
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    quantity = models.PositiveBigIntegerField(default=1)

    price = models.DecimalField(max_digits=8, decimal_places=2)

    # Foreign Key

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):

        return 'Order Item - #' + str(self.id)