from store.models import *
from store.views import *


class Cart():
    def __init__(self, request):
        self.session = request.session
        
        #get the current session key if it exists 
        cart = self.session.get('session_key')
        
        # if user is new then create one 
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure is available in all pages 
        self.cart = cart 
            
        
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        #logic 
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
        
    def __len__(self):
        return len(self.cart)
    
    
    def get_prods(self):
        # get ids from cart 
        product_ids = self.cart.keys()
        # get ids to lookup products in model 
        products = Product.objects.filter(id__in=product_ids)
        return products
        
        
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        # get the cart
        ourcart = self.cart
        # update dictonary 
        ourcart[product_id] = product_qty
        
        self.session.modified = True
        
        thing = self.cart
        return thing
    
    
    
    
    
    
    
    
    
    
    
    
    