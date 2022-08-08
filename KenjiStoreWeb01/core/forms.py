'''Este archivo no es parte de la estructura básica de Django. Se crea para trabajar los formularios de la página creados y por crear'''

'''Se importa modelo User creado en models.py'''
from django.contrib.auth.forms import UserCreationForm

from django import forms

from django.forms import ModelForm

from .models import Customer
from .models import Item
from .models import ShippingAddress

class UpdateAccountForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['username','first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Email',
        }
'''Se crea la clase de nombre CustomUserCreationForm'''
class FormularioRegistro(UserCreationForm):
    class Meta:
        model = Customer
        fields = ["username", "first_name", "last_name", "email"]
        labels = {
            "username": "Nombre de usuario",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Correo electrónico",
        }
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control'}),
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.TextInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            "username": "",
            "first_name": "",
            "last_name": "",
            "email": "",
            "password1": "",
            "password2": "",
        }

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['nombre', 'autor', 'editorial', 'precio', 'imagen', 'stock', 'descripcion', 'digital']
        labels = {
            'nombre': 'Nombre',
            'autor': 'Autor',
            'editorial': 'Editorial',
            'precio': 'Precio',
            'imagen': 'Imagen',
            'stock': 'Stock',
            'descripcion': 'Descripción',
            'digital': 'Digital',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'editorial': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'nombre': '',
            'autor': '',
            'editorial': '',
            'precio': '',
            'imagen': '',
            'stock': '',
            'descripcion': '',
            'digital': '',
        }


class ShippingForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['customer', 'boleta', 'address', 'country', 'city', 'state', 'comuna', 'zipcode',
                'street_number', 'block_number', 'phone_number']


