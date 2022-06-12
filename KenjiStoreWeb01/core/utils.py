import json
from .models import *


def cookieCart(request):
		#Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
	cartItems = order['get_cart_items']

	for i in cart:
		#We use try block to prevent items in cart that may have been removed from causing error
		try:
			cartItems += cart[i]['quantity']

			product = Item.objects.get(id=i)
			total = (item.price * cart[i]['quantity'])

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']

			item = {
				'id':item.id,
				'product':{'id':item.id,'name':item.name, 'price':item.price, 
				'image':item.imagen}, 'quantity':cart[i]['quantity'],
				'digital':item.digital,'get_total':total,
				}
			items.append(item)

			if item.digital == False:
				order['shipping'] = True
		except:
			pass