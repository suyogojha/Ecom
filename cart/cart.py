from store.models import *
from store.views import *


class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
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
        
		# Deal with logged in user
        if self.request.user.is_authenticated:
			# Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
            current_user.update(old_cart=str(carty))
        
        
        
        
    def __len__(self):
        return len(self.cart)
    
    
    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    # for sale price 
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
                        
        return total        
    
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

            # Get cart
            ourcart = self.cart
            # Update Dictionary/cart
            ourcart[product_id] = product_qty

            self.session.modified = True
        

            # Deal with logged in user
            if self.request.user.is_authenticated:
                # Get the current user profile
                current_user = Profile.objects.filter(user__id=self.request.user.id)
                # Convert {'3':1, '2':4} to {"3":1, "2":4}
                carty = str(self.cart)
                carty = carty.replace("\'", "\"")
                # Save carty to the Profile Model
                current_user.update(old_cart=str(carty))


            thing = self.cart
            return thing
    
    
    
    def delete(self, product):
            product_id = str(product)
            # Delete from dictionary/cart
            if product_id in self.cart:
                del self.cart[product_id]

            self.session.modified = True

            # Deal with logged in user
            if self.request.user.is_authenticated:
                # Get the current user profile
                current_user = Profile.objects.filter(user__id=self.request.user.id)
                # Convert {'3':1, '2':4} to {"3":1, "2":4}
                carty = str(self.cart)
                carty = carty.replace("\'", "\"")
                # Save carty to the Profile Model
                current_user.update(old_cart=str(carty))
        
    def db_add(self, product, quantity):
            product_id = str(product)
            product_qty = str(quantity)
            # Logic
            if product_id in self.cart:
                pass
            else:
                #self.cart[product_id] = {'price': str(product.price)}
                self.cart[product_id] = int(product_qty)

            self.session.modified = True

            # Deal with logged in user
            if self.request.user.is_authenticated:
                # Get the current user profile
                current_user = Profile.objects.filter(user__id=self.request.user.id)
                # Convert {'3':1, '2':4} to {"3":1, "2":4}
                carty = str(self.cart)
                carty = carty.replace("\'", "\"")
                # Save carty to the Profile Model
                current_user.update(old_cart=str(carty))  
    
    
    
    
    
    
    
    
    
    