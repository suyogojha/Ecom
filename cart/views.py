from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import *
from django.http import JsonResponse


# Create your views here.
def cart_summary(request):
    # get the cart 
    cart = Cart(request)
    cart_products = cart.get_prods
    #show card number in cart 
    quantities = cart.get_quants
    
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities})

def cart_add(request):
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        #get STUFF
        product_id = int(request.POST.get('product_id'))

        # cart_quantity 
        product_qty = int(request.POST.get('product_qty'))
        
        
        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)
        # save the session
        cart.add(product=product, quantity=product_qty)

        # get cart quantity 
        cart_quantity = cart.__len__()
        
        #return response
        # response = JsonResponse({'Product Name': product.name})
        response = JsonResponse({'qty': cart_quantity})
        return response
        

    return render(request, "cart_add.html", {})

def cart_delete(request):
    return render(request, "cart_delete.html", {})

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty':product_qty})
        return response
