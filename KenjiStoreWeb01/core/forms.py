'''Este archivo no es parte de la estructura básica de Django. Se crea para trabajar los formularios de la página creados y por crear'''

'''Se importa modelo User creado en models.py'''
from django.contrib.auth.forms import UserCreationForm

'''Se importa el modelo por defecto de Usuario de Django'''
from django.contrib.auth.models import User

from django import forms

'''Se crea la clase de nombre CustomUserCreationForm'''
class FormularioRegistro(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]