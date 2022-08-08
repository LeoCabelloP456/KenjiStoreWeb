'''Con authenticate valido que el usuari@ exista en la BD'''
from base64 import b64decode, b64encode
import email
from django.core.mail import EmailMultiAlternatives

from multiprocessing import context
import time
from venv import create
from django.contrib.auth import authenticate, login, logout
from pkg_resources import require
'''Se importa redirect para redireccionar páginas con {% url 'pagina' %}'''
from django.shortcuts import render, redirect, get_object_or_404
'''Se importa Formulario de registro'''
from django.contrib.auth.forms import UserCreationForm
'''Se importa messages para mensajes de error en registro'''
from django.contrib import messages
'''Con el * se importan TODOS los modelos de .models'''
from .models import *
'''FormularioRegistro va a reemplazar al UserCreationForm por defecto de Django'''
from .forms import FormularioRegistro, ItemForm, ShippingForm, UpdateAccountForm
'''Para restringir el acceso a templates de usuarios registrados'''
from django.contrib.auth.decorators import login_required
'''Para poder devolver el mensaje en la vista de update_item'''
from django.http import HttpResponse, JsonResponse
'''Para cargar la libería loads en la función de update_item'''
import json
'''Para mostrar la información en el transactionID'''
import datetime
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import get_user_model
from .token import account_activation_token

from . utils import cookieCart, cartData, guestOrder
# Create your views here.

def index(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'cartItems': cartItems}

    return render(request, 'core/index.html', context)


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
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # to get the domain of the current site  
            current_site = request.get_host()

            mail_subject = 'Activacion de cuenta KenjiStore'  
            message = render_to_string('emails/activation_mail.html', {  
                'user': user,  
                'domain': f"http://{current_site}",  
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token':account_activation_token.make_token(user),
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMultiAlternatives(  
                subject=mail_subject,
                body='Activacion_de_cuenta',
                to=[to_email]
            )
            email.attach_alternative(message, "text/html")
            email.send(fail_silently=False)
            
            messages.success(request, f'Su cuenta ha sido creada Exitosamente. Por favor verifique su correo para poder continuar.')

            return redirect('../login')

    context = {'form': form}
    return render(request, 'core/registro.html', context)

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True  
        user.save()
        messages.success(request, f'Su cuenta ha sido activada correctamente. Por favor inicie sesion.')
        return redirect('/login')
    else:
        messages.success(request, f'El enlace de activacion es invalido o ha expirado.')
        return redirect('/login')

def loginPag(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

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


@csrf_exempt
def updateItem(request):
    print('test')
    data = json.loads(request.body)
    productId = data['itemId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user
    product = Item.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer,
        complete=False
    )

    orderItem, created = OrderItem.objects.get_or_create(
        order=order,
        item=product
    )

    if action == 'add' and created == False:
        orderItem.quantity = (orderItem.quantity + 1)
        
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    if order.orderitem_set.all().count() == 0:
        order.delete()

    return JsonResponse('Producto agregado', safe=False)

def delete_item(request):
    item_id = request.POST.get('item')
    cart_view_name = '../cart'

    if request.user.is_authenticated:
        customer = request.user
    
        order = Order.objects.filter(customer=customer.id,complete=False).first()
        if order is None:
            return redirect(cart_view_name)

        order_item = OrderItem.objects.filter(order=order, item = item_id).first()
        if order_item is None:
            return redirect(cart_view_name)

        order_item.delete()

        if order.orderitem_set.all().count() == 0:
            order.delete()

    return redirect(cart_view_name)


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


def transferencia(request):
    return render(request, 'core/transferencia.html')


def product_report(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'core/product_report.html', context)

def form_customers(request):
    context = {
        'form': FormularioRegistro()
    }

    if request.method=='POST':

        formulario = FormularioRegistro(request.POST)
        if formulario.is_valid:
            formulario.save()
            messages.success(request, 'Formulario enviado correctamente')
            return redirect('/listar_customers')

    return render(request, 'core/form_customers.html', context)

def form_items(request):
        context = {
            'form': ItemForm()

    }

        if request.method=='POST':

            formulario = ItemForm(request.POST)
            if formulario.is_valid:
                formulario.save()
                context['mensaje'] = "Datos guardados correctamente"
        return render(request, 'core/form_items.html', context)

def form_shippings(request):
    context = {
        'form': ShippingForm()

    }

    if request.method=='POST':

        formulario = ShippingForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            context['mensaje'] = "Datos guardados correctamente"

    return render(request, 'core/form_shippings.html', context)

def form_mod_item(request, id):
    item = Item.objects.get(id=id)
    context = {
        'form': ItemForm(instance=item)
    }
    if request.method == 'POST':
        formulario = ItemForm(data=request.POST, instance=item, files=request.FILES)
    
        if formulario.is_valid:
            formulario.save()

            context['mensaje'] = "Producto modificado correctamente"
    
    return render(request, 'core/form_mod_item.html', context)

def deleteCustomer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.delete()

    messages.success(request, 'Usuari@ eliminado correctamente')
    return redirect('/listar_customers/')


def form_mod_shipping(request, id):
    shipping = ShippingAddress.objects.get(id=id)

    estado_despacho = request.POST.get('estado_despacho')
    pais = request.POST.get('pais')
    ciudad = request.POST.get('city')
    region = request.POST.get('state')
    comuna = request.POST.get('comuna')
    direccion = request.POST.get('address')
    numero_calle = request.POST.get('street_number')
    numero_depto = request.POST.get('block_number')
    zipcode = request.POST.get('zipcode')

    shipping.estado_despacho = estado_despacho
    shipping.country = pais
    shipping.city = ciudad
    shipping.state = region
    shipping.comuna = comuna
    shipping.address = direccion
    shipping.street_number = numero_calle
    shipping.block_number = numero_depto
    shipping.zipcode = zipcode
    shipping.save()

    messages.success(request, 'Datos modificados correctamente')
    
    return redirect(to=f'/modificar_shipping/{id}')

def deleteShipping(request, id):
    shipping = ShippingAddress.objects.get(id=id)
    shipping.delete()
    return redirect(to='core/index.html')


def aboutus(request):
    return render(request, 'core/aboutus.html')

def faq(request):
    return render(request, 'core/faq.html')

@csrf_exempt
def comprar_orden(request):
    if request.method=="POST":
        data = request.body.decode('utf-8')
        data = json.loads(data)
        shipping_data = data['shippingdata']

        order_id = data['order_id']
        total = data['total']
        tipo_pago = data['tipo_pago']
        if request.user.is_authenticated:
            customer = request.user

            order = Order.objects.get(id=order_id)
            if order is None:
                return JsonResponse('Orden no encontrada', safe=False)

            boleta = Boleta.objects.create(
                customer_id = customer.id,
                email = customer.email,
                total = total,
                tipo_pago = tipo_pago,
            )

            if boleta is None:
                return JsonResponse('Error al crear boleta', safe=False)
            
            for item in order.orderitem_set.all():
                boleta_item = BoletaItem.objects.create(
                    boleta_id = boleta.id,
                    cantidad = item.quantity,
                    item_id = item.item_id
                )
                if boleta_item is None:
                    return JsonResponse('Error al crear boleta item', safe=False)
            
            ShippingAddress.objects.create(
                customer_id = customer.id,
                boleta_id = boleta.id,
                address = shipping_data['direccion'],
                country = shipping_data['pais'],
                city = shipping_data['ciudad'],
                state = shipping_data['region'],
                comuna = shipping_data['comuna'],
                zipcode = shipping_data['codigo_postal'],
                street_number = shipping_data['numero_calle'],
                block_number = shipping_data['numero_block'],
                phone_number = shipping_data['numero_telefono'],
            )

            # actualizar stock de items
            for item in order.orderitem_set.all():
                item.item.stock -= item.quantity
                item.item.save()

            order.delete()
            order.orderitem_set.all().delete()
        else:
            email = data['email']
            response = guestOrder(request, {'email': email, 'total': total, 'tipo_pago': tipo_pago}, shipping_data)
            if response == -1:
                return JsonResponse('Error al crear boleta', safe=False)        

        # return json response
    return JsonResponse("exito al crear", safe=False)

def compra_realizada(request):
    return render(request, 'core/compra_realizada.html')

def mis_compras(request):
    if not request.user.is_authenticated:
        return redirect('/index')
    
    boletas = Boleta.objects.filter(customer_id=request.user.id).order_by('-created_at')

    for boleta in boletas:
        boleta.shippingaddress = ShippingAddress.objects.filter(boleta_id=boleta.id).first()

        suma = 0
        for boleta_item in boleta.boletaitem_set.all():
            suma += boleta_item.cantidad
        boleta.cantidad = suma

    context = {
        'boletas': boletas
    }
    return render(request, 'core/mis_compras.html', context)

def detalle_compra(request,boleta_id):
    boleta_item = BoletaItem.objects.filter(boleta_id=boleta_id)
    context = {
        'boleta_item': boleta_item
    }
    return render(request, 'core/detalle_compra.html', context)


# vistas de adminstrador #

def listar_ventas(request):
    if not request.user.is_superuser:
        return redirect('/index')
    
    boletas = Boleta.objects.all().order_by('-created_at')

    for boleta in boletas:
        boleta.shippingaddress = ShippingAddress.objects.filter(boleta_id=boleta.id).first()

        suma = 0
        for boleta_item in boleta.boletaitem_set.all():
            suma += boleta_item.cantidad
        boleta.cantidad = suma
    

    context = {
        'boletas': boletas,
    }

    return render(request, 'core/listar_ventas.html', context)

def listar_detalle_venta(request,boleta_id):
    if not request.user.is_superuser:
        return redirect('/index')

    boleta_item = BoletaItem.objects.filter(boleta_id=boleta_id)
    # obtain user
    context = {
        'boleta_item': boleta_item,
        'user' : boleta_item[0].boleta.customer,
        'email' : boleta_item[0].boleta.email
    }
    return render(request, 'core/listar_detalle_venta.html', context)


def mantenedores(request):
    if not request.user.is_superuser:
        return redirect('/index')
    
    return render(request, 'core/mantenedores.html')

def deleteItem(request, id):
    if not request.user.is_superuser:
        return redirect('/index')
    
    item = Item.objects.get(id=id)
    item.delete()
    return redirect('http://127.0.0.1:8000/listar_items/')

def listar_customer(request):
    if not request.user.is_superuser:
        return redirect('/index')
    
    customers = Customer.objects.all()

    context = {'customers': customers}
    return render(request, 'core/listar_customers.html', context)

def listar_item(request):
    if not request.user.is_superuser:
        return redirect('/index')
    
    items = Item.objects.all()

    context = {'items': items}
    return render(request, 'core/listar_items.html', context)

def listar_shipping(request):
    if not request.user.is_superuser:
        return redirect('/index')
    
    shipping = ShippingAddress.objects.all()

    context = {'shipping': shipping}
    return render(request, 'core/listar_shippings.html', context)

def form_mod_customer(request, id):
    customer = Customer.objects.get(id=id)
    context = {
        'form': UpdateAccountForm(instance=customer)
    }
    if request.method == 'POST':
        formulario = UpdateAccountForm(data=request.POST, instance=customer)
    
        if formulario.is_valid:
            formulario.save()

            messages.success(request, 'Se actualizó el usuario correctamente')
            return redirect('/form_mod_customer/'+id)
    
    return render(request, 'core/form_mod_customer.html', context)

def detalle_shipping(request,shipping_id):
    shipping = ShippingAddress.objects.get(id=shipping_id)
    context = {
        'shipping': shipping,
        'user': shipping.customer
    }
    return render(request, 'core/detalle_shipping.html', context)

def modificar_shipping(request,shipping_id):
    shipping = ShippingAddress.objects.get(id=shipping_id)
    context = {
        'shipping': shipping
    }
    return render(request, 'core/modificar_shipping.html', context)

def eliminar_shipping(request,shipping_id):
    shipping = ShippingAddress.objects.get(id=shipping_id)
    shipping.delete()

    messages.success(request, 'Dirección de envío eliminada')

    return redirect('/listar_shippings/')

def generar_reporte(request):
    if not request.user.is_superuser:
        return redirect('/index')

    boletas = Boleta.objects.all().order_by('-created_at')

    for boleta in boletas:
        tipo_pago_text = ''
        if boleta.tipo_pago == 1:
            tipo_pago_text = 'Transferencia'
        elif boleta.tipo_pago == 2:
            tipo_pago_text = 'Paypal'
        
        boleta.tipo_pago_text = tipo_pago_text

        suma = 0
        for boleta_item in boleta.boletaitem_set.all():
            suma += boleta_item.cantidad
        boleta.cantidad = suma

        estado_text = ''
        shipingaddress = ShippingAddress.objects.filter(boleta_id=boleta.id).first()
        if shipingaddress is not None:
            if shipingaddress.estado_despacho == 1:
                estado_text = 'En proceso'
            elif shipingaddress.estado_despacho == 2:
                estado_text = 'En camino'
            elif shipingaddress.estado_despacho == 3:
                estado_text = 'Entregado'
        else:
            estado_text = 'error'
        
        boleta.estado_text = estado_text

    df = pd.DataFrame(columns=['id', 'tipo_pago', 'email', 'cantidad_articulos','estado_envio', 'created_at', 'total'], data=[[
        boleta.id,
        boleta.tipo_pago_text,
        boleta.email,
        boleta.cantidad,
        boleta.estado_text,
        boleta.created_at.strftime("%d/%m/%Y"),
        boleta.total
    ] for boleta in boletas])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Reporte-{time.strftime("%Y%m%d-%H%M%S")}.xlsx"'                                        
    df.to_excel(response)
    return response
   