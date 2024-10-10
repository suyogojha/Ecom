from .cart import *


# create context processor for all pages 
def cart(request):
    #return the default data from our cart 
    return{'cart': Cart(request)}