from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


'''Creación de Customer (cliente)'''
class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name

'''Modificación de clase Item para poblar la tabla desde el admin'''
class Item(models.Model): 
    nombre = models.CharField(max_length=200, unique=True, null=True)
    autor = models.CharField(max_length=200, null=True)
    editorial = models.CharField(max_length=200, null=True)
    precio = models.IntegerField(null=True)
    imagen = models.ImageField('Imagen de producto', null=True, blank=True)
    stock = models.IntegerField(null=True)
    descripcion = models.CharField(max_length=400, null=True)
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
	item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)   
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.item.precio * self.quantity
		return total


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
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
    return self.user.username