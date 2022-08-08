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
    path('cart/delete_item', views.delete_item, name="delete_item"),
    path('checkout/', views.checkout, name="checkout"),  
    path('update_item/', views.updateItem, name="update_item"),
    path('mis_compras/', views.mis_compras, name="mis_compras"),
    path('detalle_compra/<boleta_id>', views.detalle_compra, name="detalle_compra"),
    path('comprar_orden/', views.comprar_orden, name="comprar_orden"),
    path('compra_realizada/', views.compra_realizada, name="compra_realizada"),
    path('process_order/', views.processOrder, name="process_order"),
    path('product_report/', views.product_report, name="product_report"),
    path('transferencia/', views.transferencia, name="transferencia"),
    path('mantenedores/', views.mantenedores, name="mantenedores"),
    path('listar_customers/', views.listar_customer, name="listar_customers"),
    path('listar_ventas/', views.listar_ventas, name="listar_ventas"),
    path('listar_detalle_venta/<boleta_id>', views.listar_detalle_venta, name="listar_detalle_venta"),
    path('listar_items/', views.listar_item, name="listar_items"),
    path('listar_shippings/', views.listar_shipping, name="listar_shipping"),
    path('form_customers/', views.form_customers, name="form_customers"),
    path('form_items/', views.form_items, name="form_items"),
    path('form_shippings/', views.form_shippings, name="form_shppings"),
    path('form_mod_item/<id>/', views.form_mod_item, name="form_mod_item"),
    path('form_mod_customer/<id>', views.form_mod_customer, name="form_mod_customer"),
    path('form_mod_shipping/<id>', views.form_mod_shipping, name="form_mod_shipping"),
    path('form_del_item/<id>/', views.deleteItem, name="form_del_item"),
    path('form_del_customer/<customer_id>', views.deleteCustomer, name="form_del_customer"),
    path('form_del_shipping/<id>', views.deleteShipping, name="form_del_shipping"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('faq/', views.faq, name="faq"),
    path('detalle_shipping/<shipping_id>', views.detalle_shipping, name="detalle_shipping"),
    path('modificar_shipping/<shipping_id>', views.modificar_shipping, name="modificar_shipping"),
    path('eliminar_shipping/<shipping_id>', views.eliminar_shipping, name="eliminar_shipping"),
    path('generar_reporte', views.generar_reporte, name="generar_reporte"),
    path('activate_token/<uidb64>/<token>/', views.activate, name="activate"),
]