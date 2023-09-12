from decimal import Decimal

from store.models import Product

class Cart():

    def __init__(self, request):

        self.session = request.session

        # Returning user -> obtain his/her existing sesssion
        cart = self.session.get('session_key')

        # If its an old user, it will look something like that session_key': {'4': {'price': '9.99', 'qty': 1}}}
        
        # New user -> generate a new session
        if 'session_key' not in request.session:

            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, product_qty):
         
        # Make it a string because we dont need a integer id
        product_id = str(product.id)

        if product_id in self.cart:
                
            self.cart[product_id]['qty'] = product_qty

        else:

            # {'102': {'price': product_price, 'qty': product_qty}}
            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}
        
        self.session.modified = True
    
    def delete(self, product):

        # Make it a string because we dont need a integer id
        product_id = str(product)

        if product_id in self.cart:
                
            del self.cart[product_id]
        
        self.session.modified = True

    def update(self, product, qty):

        # Make it a string because we dont need a integer id
        product_id = str(product)
        product_quantity = qty

        if product_id in self.cart:
                
            self.cart[product_id]['qty'] = product_quantity
        
        self.session.modified = True

    def __len__(self):
        # Iterate through the cart dictionary to obtain each of the product
        return sum(item['qty'] for item in self.cart.values())
    

    def __iter__(self):

        all_product_id = self.cart.keys()
        
        # id__in is a built-in lookup syntax in Django's ORM (Object-Relational Mapping)
        # for querying objects based on a list of IDs.
        products = Product.objects.filter(id__in=all_product_id)

        import copy

        cart = copy.deepcopy(self.cart)
        
        for product in products:

            cart[str(product.id)]['product'] = product

        for item in cart.values():

            item['price'] = Decimal(item['price'])

            item['total'] = item['price'] * item['qty']

            yield item

    def get_total(self):

        # Iterate the cart's dictionary value, add the sum for the product*qty
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())