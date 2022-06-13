'''Con authenticate valido que el usuari@ exista en la BD'''
import email
from multiprocessing import context
from venv import create
from django.contrib.auth import authenticate, login, logout
'''Se importa redirect para redireccionar páginas con {% url 'pagina' %}'''
from django.shortcuts import render, redirect
'''Se importa Formulario de registro'''
from django.contrib.auth.forms import UserCreationForm
'''Se importa messages para mensajes de error en registro'''
from django.contrib import messages
'''Con el * se importan TODOS los modelos de .models'''
from .models import *
'''FormularioRegistro va a reemplazar al UserCreationForm por defecto de Django'''
from .forms import FormularioRegistro
'''Para restringir el acceso a templates de usuarios registrados'''
from django.contrib.auth.decorators import login_required
'''Para poder devolver el mensaje en la vista de update_item'''
from django.http import JsonResponse
'''Para cargar la libería loads en la función de update_item'''
import json
'''Para mostrar la información en el transactionID'''
import datetime

from django.views.decorators.csrf import csrf_exempt

from . utils import cookieCart, cartData, guestOrder
# Create your views here.

def index(request):
    return render(request, 'core/index.html')


def catalogo(request):
    data = cartData(request)
    cartItems = data['cartItems']
    
    items = Item.objects.all()
    context = {'items':items, 'cartItems':cartItems}
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

    context = {'form': form}
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


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'core/cart.html', context)

def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'core/checkout.html', context)


def updateItem(request):
    print('´test')
    data = json.loads(request.body)
    productId = data['itemId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Item.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, item=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Producto agregado', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(data)
    
    total = float(data['form']['total'])    #igual creo que no debiese ser con float, ya que son números enteros la cantidad total
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            country = data['shipping']['country'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            comuna = data['shipping']['comuna'],
            zipcode = data['shipping']['zipcode'],
            street_number = data['shipping']['street_number'],
            block_number = data['shipping']['block_number'],
            phone_number = data['shipping']['phone_number'],
        )

    return JsonResponse('Pago completo...', safe=False)


'''
def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    items = Item.object.all()
    context = {'items': items, 'cartItems': cartItems}
    return render(request, 'core/store.html', context)
'''

'''definimos una función para el producto'''
# pasar por url a la vista

'''
def single_producto(request, pk):
    context = {}
    # crear template producto
    productos = Item.objects.filter(pk=pk).first()
    # validar que tenga producto ( get object or 404)

    context['single_producto'] = productos
    return render(request, "core/productos/single_producto.html",
                  context)  # hacer template producto detalle
'''