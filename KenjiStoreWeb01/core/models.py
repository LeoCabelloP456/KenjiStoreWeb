from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser


'''Creación de Customer (cliente)'''
class Customer(AbstractUser):
	username = models.CharField(max_length=200, null=False)
	first_name = models.CharField(max_length=200, null=False)
	last_name = models.CharField(max_length=200, null=True)
	email = models.EmailField(max_length=254, unique=True)

	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ["username", "name", "password2"]

	def __str__(self):
		return self.username or ' '

'''Modificación de clase Item para poblar la tabla desde el admin'''
class Item(models.Model): 
    autor = models.CharField(max_length=200, null=True)
    descripcion = models.CharField(max_length=400, null=True)
    editorial = models.CharField(max_length=200, null=True)
    imagen = models.ImageField('Imagen de producto', null=True, blank=True)
    nombre = models.CharField(max_length=200, null=True)
    precio = models.IntegerField(null=True)
    stock = models.IntegerField(null=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    def __str__(self):
	    return self.nombre


class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
	
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.item.digital == False:
				shipping = True
		return shipping

	
	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total


class OrderItem(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)   
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	quantity = models.IntegerField(default=1, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.item.precio * self.quantity
		return total

class Boleta(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	email = models.CharField(max_length=200, null=False)
	total = models.IntegerField(null=False, default=1)
	tipo_pago = models.IntegerField(null=False, default=1) #1 = transferencia, 2 = paypal
	
	# timestamps
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.email

class BoletaItem(models.Model):
	boleta = models.ForeignKey(Boleta, on_delete=models.SET_NULL, null=True)
	item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
	cantidad = models.IntegerField(null=False, default=1)
	
	# timestamps
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.id)

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True) # usuario anonimo
	boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE, null=True)

	estado_despacho = models.IntegerField(null=False, default=1) # 1 = en proceso, 2 = en camino, 3 = entregado
	address = models.CharField(max_length=200, null=True)
	country = models.CharField(max_length=200, null=True)
	city = models.CharField(max_length=200, null=True)
	state = models.CharField(max_length=200, null=True)    #región en el formulario de checkout
	comuna = models.CharField(max_length=200, null=True)   
	zipcode = models.CharField(max_length=200, null=True)
	street_number = models.CharField(max_length=200, null=True)
	block_number = models.CharField(max_length=200, null=True)
	phone_number = models.CharField(max_length=200, null=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address


'''Para mostrar el nombre del usuario creado en el panel admin -> tabla Users'''
def __str__(self):
    return self.customer.name