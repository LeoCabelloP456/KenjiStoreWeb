from django.urls import path
from . import views
from django.urls import path
from .views import registro, stock

urlpatterns = [
    path('', views.store, name="store"),
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('login/', views.login, name="login"),
    path('stock/', stock, name="stock"),
    path('registro/', registro, name="registro"),

]