from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import *
from django.http import JsonResponse


# Create your views here.
def cart_summary(request):
    # get the cart 
    cart = Cart(request)
    cart_products = cart.get_prods
    return render(request, "cart_summary.html", {"cart_products": cart_products})

def cart_add(request):
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        #get STUFF
        product_id = int(request.POST.get('product_id'))
        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)
        # save the session
        cart.add(product=product)

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
    return render(request, "cart_update.html", {})

