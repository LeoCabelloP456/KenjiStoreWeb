from sre_constants import CATEGORY
from unicodedata import category
from django.db import models
from django.conf import settings

# Create your models here.

'''CATEGORY_CHOICES = (
    ('', '')
)'''

'''LABEL_CHOICES = (
    ('', '')
)'''



class Item(models.Model): 
    title = models.CharField(max_length=100)
    price = models.FloatField()
    '''category = models.Charfield(choices= CATEGORY_CHOICES, max_length=1)'''

    def __str__(self):
        return super().__str__()

class OrderItem (models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return super().__str__()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                            on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

'''Creación de la tabla Producto
class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre de articulo', max_length=200)
    descripcion = models.CharField('Descripcion', max_length=200)
    autor = models.CharField('Autor', max_length=200)
    precio = models.IntegerField('Precio')
    editorial = models.CharField('Editorial', max_length=200)
    cantidad_pag = models.IntegerField('Cantidad paginas')
    isbn = models.IntegerField('Isbn')
'''

'''Para mostrar el nombre del usuario creado en el panel admin -> tabla Users'''
def __str__(self):
    return self.user.username