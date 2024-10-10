from django.shortcuts import render, redirect
from .models import *
from .forms import *
# login
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# register
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request, 'about.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user  = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have logged IN.."))
            return redirect('home')
        else:
            messages.success(request, ("There was error try again.."))
            return redirect('login')
            
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have logged out.."))
    return redirect('home')



def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # loginuser
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have registered"))
            return redirect('home')
        else:
            messages.success(request, ("You have problem"))
            return redirect('register')

    else:
        return render(request, 'register.html', {'form':form})




def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})
    

    

def category(request, foo):
    # replace hyphens with spaces in url 
    foo = foo.replace('-', ' ')
    #grab the category from the url 
    try:
        #look to category 
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category': category})
        
    except:
        messages.success(request, ("You Dont have category"))
        return redirect('homes')
    





