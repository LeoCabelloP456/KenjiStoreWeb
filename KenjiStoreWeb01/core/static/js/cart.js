var updateBtns = document.getElementsByClassName('update-cart')


for (const element of updateBtns) {
	element.addEventListener('click', function () {
		
		var itemId = this.dataset.item;
		var itemStock = this.dataset.item_stock;
		var action = this.dataset.action;
		console.log('itemId: ', itemId)
		console.log('itemStock: ', itemStock)
		console.log('action:', action)	

		if (user == 'AnonymousUser') {
			if (action === 'add') {
				addCookieItem(itemId, action, itemStock)
			}

			if (action === 'remove') {
				addCookieItem(itemId, action, itemStock)
			}

			if (action == 'delete') {
				deleteCookieItem(itemId)
			}
		} else {
			updateUserOrder(itemId, action, itemStock);
		}


	})
}

function deleteCookieItem(itemId) {
	delete cart[itemId];

	document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
	location.reload();

}

function updateUserOrder(itemId, action, itemStock) {
	var csrf_token = jQuery("[name=csrfmiddlewaretoken]").val();
	//console.log('Usuario autenticado. Enviando datos...')

	var url = '/update_item/';

	fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrf_token,
			},
			body: JSON.stringify({
				'itemId': itemId,
				'action': action
			})
		})
		.then((response) => {
			return response.json();
		})
		.then((data) => {
			console.log('data: ', data);
			location.reload();
		});
}


function addCookieItem(itemId, action, itemStock) {
	if (action == 'add') {
		console.log('Agregando al carrito')
		if (cart[itemId] === undefined) {
			cart[itemId] = {
				'quantity': 1
			}
		} else {
			if (itemStock > cart[itemId].quantity) {
				cart[itemId].quantity += 1;
			}
		}
	}

	if (action === 'remove') {
		cart[itemId]['quantity'] -= 1

		if (cart[itemId]['quantity'] <= 0) {
			delete cart[itemId];
		}
	}
	console.log('CART:', cart)
	document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
	location.reload();

}
