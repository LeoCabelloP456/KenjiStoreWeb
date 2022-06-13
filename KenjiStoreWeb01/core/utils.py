import json
from . models import *


def cookieCart(request):
		# Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}

	print('Cart:', cart)
	items = []
	order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
	cartItems = order['get_cart_items']

	for i in cart:
		try:
			cartItems += cart[i]['quantity']

			item = Item.objects.get(id=i)
			total = (item.precio * cart[i]['quantity'])

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']

			item = {
                'product': {
                    'id': item.id,
                    'name': item.name,
                    'price': item.precio,
                    'image': item.imagen
                    },
                'quantity': cart[i]['quantity'],
                'get_total': total
                }
			items.append(item)

		except:
			pass
	return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(
		    customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
	print('El usuario aún no ha iniciado sesión')

	print('COOKIES:', request.COOKIES)
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
		email=email,
		)
	customer.name = name
	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)

	for item in items:
		item = Item.objects.get(id=item['product']['id'])

		orderItem = OrderItem.objects.create(
			item=item,
			order=order,
			quantity=item['quantity']
		)
	return customer, order 