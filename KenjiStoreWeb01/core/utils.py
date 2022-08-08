import json
from . models import *

class CustomOrderItem:
	def __init__(self, quantity, item):
		self.quantity = quantity
		self.item = item

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

			item = CustomOrderItem(cart[i]['quantity'], item)
			items.append(item)
		except Exception as e:
			print("------------------------error-------------------------")
			print(e)
			

	return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.id
		order = Order.objects.filter(customer=customer, complete=False).first()

		cart_items = 0
		items = None
		if order is not None:
			cart_items = order.get_cart_items
			items = order.orderitem_set.all()
	else:
		cookie_data = cookieCart(request)
		cart_items = cookie_data['cartItems']
		order = cookie_data['order']
		items = cookie_data['items']

	return {'cartItems': cart_items, 'order': order, 'items': items}


def guestOrder(request, data, shipping_data):
	cookie_data = cookieCart(request)
	items = cookie_data['items']

	boleta = Boleta.objects.create(
		customer_id = None,
		email = data["email"],
		total = data["total"],
		tipo_pago = data["tipo_pago"],
	)

	if boleta is None:
		return -1

	for item in items:
		boleta_item = BoletaItem.objects.create(
		boleta_id = boleta.id,
		cantidad = item.quantity,
		item_id = item.item.id
	)
	if boleta_item is None:
		return -1

	ShippingAddress.objects.create(
		customer_id = None,
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
	for item in items:
		item.item.stock -= item.quantity
		item.item.save()

	return 0
