from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate

def home(request):    
    data = 'Saytda texnik ishlar olib borilmaoqda'
    contex = {
        'data':data,
    }
    return render(request, 'asosiy/home.html', contex)



@csrf_exempt
def kirish(request):
    data = 'Kirish sahifasi'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user.save()
            return redirect('/')
        else:
            messages.warning(request, 'Id yoki parol xato')
            return redirect('/kirish') 
            
    contex = {
        'data':data,
    }
    return render(request, 'asosiy/kirish.html', contex)

def royhat(request):
    data = 'Ro`yhatdan o`tish sahifasi'
    contex = {
        'data':data,
    }
    return render(request, 'asosiy/royhat.html', contex)

def dekanatadmin(request):
    data = 'Dekanat admin asosiy sahifasi'
    contex = {
        'data':data,
    }
    return render(request, 'dekanatadmin/home.html', contex)

def superadmin(request):
    data = 'Super admin asosiy sahifasi'
    contex = {
        'data':data,
    }
    return render(request, 'superadmin/home.html', contex)

def talaba(request):
    data = 'talaba asosiy shifasiga hush kelibsiz'
    contex = {
        'data':data,
    }
    return render(request, 'talaba/home.html', contex)