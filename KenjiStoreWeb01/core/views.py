from multiprocessing import context

'''Con authenticate valido que el usuari@ exista en la BD'''
from django.contrib.auth import authenticate, login, logout

'''Se importa redirect para redireccionar páginas con {% url 'pagina' %}'''
from django.shortcuts import render, redirect



'''Se importa Formulario de registro'''
from django.contrib.auth.forms import UserCreationForm

'''Se importa messages para mensajes de error en registro'''
from django.contrib import messages

# Create your views here.
'''Con el * se importan TODOS los modelos de .models'''
from .models import *

'''FormularioRegistro va a reemplazar al UserCreationForm por defecto de Django'''
from .forms import FormularioRegistro

'''Para restringir el acceso a templates de usuarios registrados'''
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'core/index.html')


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

            return redirect('../login')

    context = {'form':form}
    return render(request, 'core/registro.html', context)

def loginPag(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password')

        user = authenticate(request, username=username, password=password1)

        if user is not None:
            login(request, user)
            return redirect('../index')
        else:
            messages.info(request, 'Usuario o contraseña incorrecta')

    context = {}
    return render(request, 'core/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('../login')


'''definimos una función para el producto'''
# pasar por url a la vista

def single_producto(request, pk=None):
    context = {}
    # crear template producto
    productos = Item.objects.filter(pk=pk, item_id=request.id).first()
    # validar que tenga producto ( get object or 404)


    context[Item] = productos
    return render(request, "core/productos/single_producto.html", context) 


def producto_ejemplo(request):
    context = {    }
    return render(request, "core/productos/producto_ejemplo.html", context)
