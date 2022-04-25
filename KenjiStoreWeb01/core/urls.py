from django.urls import path
from . import views
from django.urls import path

urlpatterns = [
    path('', views.store, name="store"),
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('login/', views.login, name="login"),
    path('stock/', views.stock, name="stock"),
]