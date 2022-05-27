from django.urls import path
from django.contrib import admin  
from .views import index, registroPag, loginPag, catalogo, producto1, producto2, producto3, producto4, producto5, producto6, producto7, producto8


app_name = 'core'

urlpatterns = [
    path ('', index, name= "index"),
    path('catalogo/', catalogo, name = 'lista_catalogo'),

    path('registro/', registroPag, name="registro"),
    path('login/', loginPag, name="login"),
    path('producto1/', producto1, name="producto1"),
    path('producto2/', producto2, name="producto2"),
    path('producto3/', producto3, name="producto3"),
    path('producto4/', producto4, name="producto4"),
    path('producto5/', producto5, name="producto5"),
    path('producto6/', producto6, name="producto6"),
    path('producto7/', producto7, name="producto7"),
    path('producto8/', producto8, name="producto")
]

 