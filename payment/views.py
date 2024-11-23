from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile
import datetime
from django.conf import settings
from uuid import uuid4
# Import Some Paypal Stuff
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid # unique user id for duplictate orders

def orders(request, pk):
	if request.user.is_authenticated and request.user.is_superuser:
		# Get the order
		order = Order.objects.get(id=pk)
		# Get the order items
		items = OrderItem.objects.filter(order=pk)

		if request.POST:
			status = request.POST['shipping_status']
			# Check if true or false
			if status == "true":
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				now = datetime.datetime.now()
				order.update(shipped=True, date_shipped=now)
			else:
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				order.update(shipped=False)
			messages.success(request, "Shipping Status Updated")
			return redirect('home')


		return render(request, 'payment/orders.html', {"order":order, "items":items})




	else:
		messages.success(request, "Access Denied")
		return redirect('home')



def not_shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=False)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# Get the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=True, date_shipped=now)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')

		return render(request, "payment/not_shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')

def shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=True)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# grab the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=False)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')


		return render(request, "payment/shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')

def process_order(request):
	if request.POST:
		# Get the cart
		cart = Cart(request)
		cart_products = cart.get_prods
		quantities = cart.get_quants
		totals = cart.cart_total()

		# Get Billing Info from the last page
		payment_form = PaymentForm(request.POST or None)
		# Get Shipping Session Data
		my_shipping = request.session.get('my_shipping')

		# Gather Order Info
		full_name = my_shipping['shipping_full_name']
		email = my_shipping['shipping_email']
		# Create Shipping Address from session info
		shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
		amount_paid = totals

		# Create an Order
		if request.user.is_authenticated:
			# logged in
			user = request.user
			# Create Order
			create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
			create_order.save()

			# Add order items
			
			# Get the order ID
			order_id = create_order.pk
			
			# Get product Info
			for product in cart_products():
				# Get product ID
				product_id = product.id
				# Get product price
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price

				# Get quantity
				for key,value in quantities().items():
					if int(key) == product.id:
						# Create order item
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
						create_order_item.save()

			# Delete our cart
			for key in list(request.session.keys()):
				if key == "session_key":
					# Delete the key
					del request.session[key]

			# Delete Cart from Database (old_cart field)
			current_user = Profile.objects.filter(user__id=request.user.id)
			# Delete shopping cart in database (old_cart field)
			current_user.update(old_cart="")


			messages.success(request, "Order Placed!")
			return redirect('home')

			

		else:
			# not logged in
			# Create Order
			create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
			create_order.save()

			# Add order items
			
			# Get the order ID
			order_id = create_order.pk
			
			# Get product Info
			for product in cart_products():
				# Get product ID
				product_id = product.id
				# Get product price
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price

				# Get quantity
				for key,value in quantities().items():
					if int(key) == product.id:
						# Create order item
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
						create_order_item.save()

			# Delete our cart
			for key in list(request.session.keys()):
				if key == "session_key":
					# Delete the key
					del request.session[key]



			messages.success(request, "Order Placed!")
			return redirect('home')


	else:
		messages.success(request, "Access Denied")
		return redirect('home')





def billing_info(request):
    if request.method == "POST":
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Create a session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']

        # Create Shipping Address from session info
        shipping_address = (
            f"{my_shipping['shipping_address1']}\n"
            f"{my_shipping['shipping_address2']}\n"
            f"{my_shipping['shipping_city']}\n"
            f"{my_shipping['shipping_state']}\n"
            f"{my_shipping['shipping_zipcode']}\n"
            f"{my_shipping['shipping_country']}"
        )
        amount_paid = totals

        # Get the host
        host = request.get_host()

        # Create PayPal Form Dictionary
        my_invoice = str(uuid4())
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': totals,
            'item_name': 'Book Order',
            'no_shipping': '2',
            'invoice': my_invoice,
            'currency_code': 'USD',  # EUR for Euros
            'notify_url': f'https://{host}{reverse("paypal-ipn")}',
            'return_url': f'https://{host}{reverse("payment_success")}',
            'cancel_return': f'https://{host}{reverse("payment_failed")}',
        }

        # Create actual PayPal button
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)

        # Function to create order items
        def create_order_items(order_id, user=None):
            for product in cart_products():
                product_id = product.id
                price = product.sale_price if product.is_sale else product.price

                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(
                            order_id=order_id,
                            product_id=product_id,
                            user=user,
                            quantity=value,
                            price=price,
                        )
                        create_order_item.save()

        # Check if the user is logged in
        if request.user.is_authenticated:
            # Logged in
            user = request.user
            billing_form = PaymentForm()

            # Create order
            create_order = Order(
                user=user,
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid,
                invoice=my_invoice,
            )
            create_order.save()

            # Add order items
            create_order_items(create_order.pk, user=user)

            # Clear old cart in user profile
            Profile.objects.filter(user__id=user.id).update(old_cart="")

            return render(
                request,
                "payment/billing_info.html",
                {
                    "paypal_form": paypal_form,
                    "cart_products": cart_products,
                    "quantities": quantities,
                    "totals": totals,
                    "shipping_info": request.POST,
                    "billing_form": billing_form,
                },
            )

        else:
            # Not logged in
            billing_form = PaymentForm()

            # Create order
            create_order = Order(
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid,
                invoice=my_invoice,
            )
            create_order.save()

            # Add order items
            create_order_items(create_order.pk)

            return render(
                request,
                "payment/billing_info.html",
                {
                    "paypal_form": paypal_form,
                    "cart_products": cart_products,
                    "quantities": quantities,
                    "totals": totals,
                    "shipping_info": request.POST,
                    "billing_form": billing_form,
                },
            )

    else:
        messages.error(request, "Access Denied")
        return redirect('home')
    
    
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect   
    

def checkout(request):
    # Add a login message if the user is redirected here
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in first to proceed to checkout.")
        return redirect('/register/')  # Redirect to registration or login page

    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    try:
        # Retrieve the user's shipping address if available
        shipping_user = ShippingAddress.objects.get(user=request.user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    except ShippingAddress.DoesNotExist:
        # If no existing shipping address, create a blank form
        shipping_form = ShippingForm(request.POST or None)

    return render(request, "payment/checkout.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "shipping_form": shipping_form,
    })
	

def payment_success(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods  # Assumes this is a callable or iterable
    quantities = cart.get_quants  # Assumes this is a callable or dict-like
    totals = cart.cart_total()

    # Clear specific session key if it exists
    if "session_key" in request.session:
        del request.session["session_key"]

    # Render the payment success page
    return render(
        request,
        "payment/payment_success.html",
        {
            "cart_products": cart_products,
            "quantities": quantities,
            "totals": totals,
        },
    )



def payment_failed(request):
	return render(request, "payment/payment_failed.html", {})