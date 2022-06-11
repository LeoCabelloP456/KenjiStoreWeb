var updateBtns = document.getElementsByClassName('update-cart')


for (var i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var itemId = this.dataset.item
		var action = this.dataset.action
		console.log(action)
		console.log('itemId:', itemId, 'action:', action)
    
        
        console.log('USER:', user)
        if (user == 'AnonymousUser'){
            console.log('El usuario no está autenticado')
                    
        }else{
			console.log('Test')
            updateUserOrder(itemId, action)
        }

	})
}

function updateUserOrder(itemId, action){
	var csrf_token = jQuery("[name=csrfmiddlewaretoken]").val();
	console.log(csrf_token) 
	//console.log('Usuario autenticado. Enviando datos...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken': csrf_token,
			}, 
			body:JSON.stringify({'itemId':itemId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
            console.log('data: ', data)
		    location.reload()
		});
}