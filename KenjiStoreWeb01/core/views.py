from django.shortcuts import render

# Create your views here.
def store(request):
    context = {}
    return render(request, 'core/store.html', context)

def cart(request):
    context = {}
    return render(request, 'core/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'core/checkout.html', context)

def login(request):
    context = {}
    return render(request, 'core/login.html', context)

def stock(request):
    context = {}
    return render(request, 'core/stock.html', context)

def stock(request):
    context = {}
    return render(request, 'register/register.html', context)
