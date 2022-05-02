from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib import messages


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

def stock(request):
    context = {}
    return render(request, 'core/stock.html', context)

def registro(request):
    data = {
        'form' : CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password = formulario.cleaned_data["password1"],)
            login(request,user)
            messages.success(request, "Te has registrado correctamente")
            return redirect(to="main")
        data["form"] = formulario 

    return render(request, 'core/registro.html', data)
