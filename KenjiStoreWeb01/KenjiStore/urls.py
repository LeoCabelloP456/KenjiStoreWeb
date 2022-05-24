"""KenjiStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('allauth.urls')),
    path('catalogo/', include('core.urls', namespace= 'core1')),
    path('producto1/', include('core.urls', namespace= 'producto1')),
    path('producto2/', include('core.urls', namespace= 'producto2')),
    path('producto3/', include('core.urls', namespace= 'producto3')),
    path('producto4/', include('core.urls', namespace= 'producto4')),
    path('producto5/', include('core.urls', namespace= 'producto5')),
    path('producto6/', include('core.urls', namespace= 'producto6')),
    path('producto7/', include('core.urls', namespace= 'producto7')),
    path('producto7/', include('core.urls', namespace= 'producto7')),
]

'''if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]'''