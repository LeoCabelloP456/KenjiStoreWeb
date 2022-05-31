from django.urls import path
from django.contrib import admin  
from . import views 


app_name = 'core'

urlpatterns = [
    path ('', views.index, name= "index"),
    path('catalogo/', views.catalogo, name = 'lista_catalogo'),

    path('registro/', views.registroPag, name="registro"),
    path('login/', views.loginPag, name="login"),

    path('producto1/', views.producto1, name="producto1"),
    path('producto2/', views.producto2, name="producto2"),
    path('producto3/', views.producto3, name="producto3"),
    path('producto4/', views.producto4, name="producto4"),
    path('producto5/', views.producto5, name="producto5"),
    path('producto6/', views.producto6, name="producto6"),
    path('producto7/', views.producto7, name="producto7"),
    path('producto8/', views.producto8, name="producto"),
    # crear url detalle producto
    #path('producto/<int:pk>', views.producto, name="producto"),

]

 