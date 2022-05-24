from multiprocessing import context
from django.contrib.auth import authenticate, login, logout

'''Se importa redirect para redireccionar páginas con {% url 'pagina' %}'''
from django.shortcuts import render, redirect

'''Para complementar con la redirección de url'''
from django.http import HttpResponse

'''Se importa Formulario de registro'''
from django.contrib.auth.forms import UserCreationForm

'''Se importa messages para mensajes de error en registro'''
from django.contrib import messages

# Create your views here.
'''Con el * se importan TODOS los modelos de .models'''
from .models import *

'''FormularioRegistro va a reemplazar al UserCreationForm por defecto de Django'''
from .forms import FormularioRegistro


def index(request):
    context = {}
    return render(request, 'core/index.html', context)


def catalogo(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "core/catalogo.html", context)

def registroPag(request):
    form = FormularioRegistro()

    if request.method == 'POST':
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            form.save()
            '''La línea de de abajo me permite obtner el nombre de usuario para mostrarlo en el mensaje exitoso de cuenta creada'''
            user = form.cleaned_data.get('username')
            messages.success(request, 'Tu cuenta ha sido creada, ' + user)

            return redirect('login')

    context = {'form':form}
    return render(request, 'core/registro.html', context)

def loginPag(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password')

        user = authenticate(request, username=username, password=password1)

        if user is not None:
            login(request, user)
            return redirect('index')

    context = {}
    return render(request, 'core/login.html', context)


'''definimos una función para cada producto'''
def producto1(request):
    context = {    }
    return render(request, "core/productos/producto1.html", context)

def producto2(request):
    context = {    }
    return render(request, "core/productos/producto2.html", context)

def producto3(request):
    context = {    }
    return render(request, "core/productos/producto3.html", context)

def producto4(request):
    context = {    }
    return render(request, "core/productos/producto4.html", context)

def producto5(request):
    context = {    }
    return render(request, "core/productos/producto5.html", context)

def producto6(request):
    context = {    }
    return render(request, "core/productos/producto6.html", context)

def producto7(request):
    context = {    }
    return render(request, "core/productos/producto7.html", context)

def producto8(request):
    context = {    }
    return render(request, "core/productos/producto8.html", context)