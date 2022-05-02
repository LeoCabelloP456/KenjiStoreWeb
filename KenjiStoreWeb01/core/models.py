from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField('Nombre de usuario', max_length=30)
    first_name = models.CharField('Nombre', max_length=10)
    last_name = models.CharField('Apellido', max_length=20)
    email = models.EmailField('Correo', max_length=20)
    password1 = models.CharField('Contraseña', max_length=20)
    password2 = models.CharField('Contraseña', max_length=20)

