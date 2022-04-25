from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login

'''Clase para crear formulario'''
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

'''def authentication(request):
    context = {}
    return render(request, 'register/register.html', context)'''


class VistaRegistro(View):

    '''gestiona el get y visualización del formulario de registro'''
    def get(self, request):
        form=UserCreationForm()
        return render(request, 'register/register.html',{'form':form}) 

    '''para enviar data a la BD'''    
    def post(self, request):
        form=UserCreationForm(request.POST) #Para almacenar la data ingresada en el formulario#

        if form.is_valid():

            usuario=form.save()

            login(request, usuario)

            return redirect('store')
        else:
            pass

