from django.shortcuts import render

# Create your views here.
def home(request):
    a = 1
    b = 2
    return render(request, 'home.html', {})