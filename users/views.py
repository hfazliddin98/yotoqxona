from django.shortcuts import render

def home(request):    
    data = 'Saytda texnik ishlar olib borilmaoqda'
    contex = {
        'data':data,
    }
    return render(request, 'home.html', contex)
