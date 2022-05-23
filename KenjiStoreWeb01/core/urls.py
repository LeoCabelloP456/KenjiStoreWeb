from django.urls import path
from . import views

from django.contrib import admin  
from .views import catalogo, productos


app_name = 'core'

urlpatterns = [
    path('', views.index, name="index"),
    path('catalogo/', catalogo, name = 'lista_catalogo'),

    path('registro/', views.registroPag, name="registro"),
    path('login/', views.loginPag, name="login"),
    path('productos/', productos, name="productos"),
]

 