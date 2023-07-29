from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate, get_user_model
from users.models import User
from ariza.models import Ariza, Barcha_tolov, Tolov

@csrf_exempt
def home(request):    
    data = User.objects.filter(id=request.user.id)
    ariza = Ariza.objects.all()
    barcha_tolovlar = Barcha_tolov.objects.all()
    tasdiqlangan_tolov = Tolov.objects.filter(tasdiqlash='tasdiqlandi')
    if barcha_tolovlar :        
        for b in barcha_tolovlar:        
            yillik = int(b.xonalar_soni)*int(b.yillik_tolov)
            xonalar = int(b.xonalar_soni)
            ttj = int(b.ttj_soni)        
    else:               
        yillik = 0
        xonalar = 0
        ttj = 0 
        
    if tasdiqlangan_tolov:
        tolovlar = 0
        for t in tasdiqlangan_tolov:            
            tolovlar += int(t.narhi) 
      
    else:
        tolovlar = 0       
    
        
    contex = {
        'data':data,
        'ariza':ariza,
        'yillik':yillik,
        'ttj':ttj,
        'xonalar':xonalar,
        'tolovlar':tolovlar,
      
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

@csrf_exempt
def royhat(request):
    data = 'Ro`yhatdan o`tish sahifasi'
    habar = ''
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        sharif = request.POST['sharif']        
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if User.objects.filter(username=username):
            habar = 'Bunday telefon raqam mavjud'                  
        else:
            user = get_user_model().objects.create(
                lavozim='talaba', username = username, last_name = last_name, 
                first_name = first_name, sharif=sharif,
                password = make_password(password1), parol=password2
            )
            user.is_active = False
            user.is_staff = False 
            return redirect('/')  
    contex = {
        'data':data,
        'habar':habar,
    }
    return render(request, 'asosiy/royhat.html', contex)

@csrf_exempt
def superadmin_qoshish(request):
    data = 'Ro`yhatdan o`tish sahifasi'
    habar = ''
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        sharif = request.POST['sharif']        
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if User.objects.filter(username=username):
            habar = 'Bunday telefon raqam mavjud'                  
        else:
            user = get_user_model().objects.create(
                lavozim='super', username = username, last_name = last_name, 
                first_name = first_name, sharif=sharif,
                password = make_password(password1), parol=password2
            )
            user.is_active = False
            user.is_staff = False 
            return redirect('/')  
    contex = {
        'data':data,
        'habar':habar,
    }
    return render(request, 'superadmin/admin_qoshish.html', contex)


@csrf_exempt
def dekanatadmin_qoshish(request):
    data = 'Ro`yhatdan o`tish sahifasi'
    habar = ''
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        sharif = request.POST['sharif']  
        fakultet = request.POST['fakultet']       
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if User.objects.filter(username=username):
            habar = 'Bunday telefon raqam mavjud'                  
        else:
            user = User.objects.create(
                lavozim='dekanat', username = username, last_name = last_name, 
                first_name = first_name, sharif=sharif, fakultet=fakultet,
                password = make_password(password1), parol=password2
            )
            user.is_active = False
            user.is_staff = False 
            return redirect('/')  
    contex = {
        'data':data,
        'habar':habar,
    }
    return render(request, 'dekanatadmin/admin_qoshish.html', contex)

@csrf_exempt
def dekanatadmin(request):
    data = 'Dekanat admin asosiy sahifasi'
    contex = {
        'data':data,
    }
    return render(request, 'dekanatadmin/home.html', contex)

@csrf_exempt
def superadmin(request):
    data = 'Super admin asosiy sahifasi'
    contex = {
        'data':data,
    }
    return render(request, 'superadmin/home.html', contex)

@csrf_exempt
def talaba(request):
    data = 'talaba asosiy shifasiga hush kelibsiz'
    contex = {
        'data':data,
    }
    return render(request, 'talaba/home.html', contex)