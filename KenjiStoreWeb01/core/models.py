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


'''Modificación de clase Item para poblar la tabla desde el admin'''
class Item(models.Model): 
    nombre = models.CharField(max_length=45, unique=True, null=True)
    autor = models.CharField(max_length=30, null=True)
    editorial = models.CharField(max_length=45, null=True)
    precio = models.IntegerField(null=True)
    imagen = models.ImageField('Imagen de producto', upload_to= 'producto/', null=True, blank=True)
    stock = models.IntegerField(null=True)
    descripcion = models.CharField(max_length=400, null=True)
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


'''Para mostrar el nombre del usuario creado en el panel admin -> tabla Users'''
def __str__(self):
    return self.user.username