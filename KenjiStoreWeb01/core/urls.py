from django.urls import path
from django.contrib import admin  
from . import views 


app_name = 'core'

urlpatterns = [
    path ('', views.index),
    path ('index/', views.index, name= "index"),
    path('catalogo/', views.catalogo, name = 'lista_catalogo'),
    path('registro/', views.registroPag, name="registro"),
    path('login/', views.loginPag, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('cart/', views.cart, name="cart"),   
    path('producto_ejemplo/', views.producto_ejemplo, name="producto_ejemplo"),
    path('producto/<int:pk>', views.single_producto, name="single_producto"),
]

 