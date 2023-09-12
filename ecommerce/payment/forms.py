from django import forms

from . models import ShipppingAddress
class ShippingForm(forms.ModelForm):

    class Meta:

        model = ShipppingAddress

        fields = ['full_name', 'email', 'address1', 'address2', 'city', 'state', 'zipcode']

        exclude = ['user',] # Excluding this field

    