from django.shortcuts import render, redirect, get_object_or_404
from ariza.models import Ariza, Tolov, Tark_etgan
from users.models import User


def arizalar(request):
    talaba_id = request.user.id
    data = 'ariza toldirish uchun'
    if request.method == 'POST':
        viloyat = request.POST['viloyat']
        tuman = request.POST['tuman']
        kocha = request.POST['kocha']
        fakultet = request.POST['fakultet']
        yonalish = request.POST['yonalish']  
        kurs = request.POST['kurs']
        pasport_rasm = request.FILES['pasport_rasm']
        imtiyoz_nomi = request.POST['imtiyoz_nomi']
        imtiyoz_file = request.FILES['imtiyoz_file']
        
        
        ariza = Ariza.objects.create(
                talaba_id=talaba_id, viloyat = viloyat, tuman = tuman,
                kocha=kocha, fakultet = fakultet, yonalish=yonalish,
                kurs = kurs, pasport_rasm=pasport_rasm, 
                imtiyoz_nomi=imtiyoz_nomi, imtiyoz_file=imtiyoz_file,               
        ) 
        ariza.save()          
        return redirect('/')   
    contex = {
        'data':data,
    }
    return render(request, 'talaba/arizalar.html', contex)


def barcha_arizalar(request):
    talabalar = User.objects.filter(lavozim='talaba')
    arizalar = Ariza.objects.filter(tasdiqlash='')
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
    }
    return render(request, 'dekanatadmin/barcha _arizalar.html', contex)

def tasdiqlangan_ariza(request, pk):    
    talabalar = User.objects.get(id=pk)
    if request.method == 'POST':
        data = get_object_or_404(Ariza, talaba_id=pk)
        xulosa = request.POST['xulosa']  
        data.xulosa = xulosa      
        data.tasdiqlash = 'tasdiqlandi'        
        data.save()
        return redirect('/ariza/barcha_arizalar/')
    contex = {
        'talabalar':talabalar,
    }
    return render(request, 'dekanatadmin/tasdiqlangan_ariza.html', contex)


def radetilgan_ariza(request, pk):   
    talabalar = User.objects.get(id=pk)
    if request.method == 'POST':
        data = get_object_or_404(Ariza, talaba_id=pk)
        xulosa = request.POST['xulosa']  
        data.xulosa = xulosa      
        data.tasdiqlash = 'radetildi'        
        data.save()
        return redirect('/ariza/barcha_arizalar/')
    contex = {
      'talabalar':talabalar,  
    }
    return render(request, 'dekanatadmin/tasdiqlangan_ariza.html', contex)

def tasdiqlangan(request):
    data = Ariza.objects.filter(tasdiqlash='tasdiqlandi')
    contex = {
        'data':data,
    }
    return render(request,  'dekanatadmin/tasdiqlangan.html', contex)


def radetilgan(request):
    data = Ariza.objects.filter(tasdiqlash = 'radetildi')
    contex = {
        'data':data,
    }
    return render(request,  'dekanatadmin/radetilgan.html', contex)


def talaba_malumotlar(request, pk):
    talabalar = User.objects.filter(lavozim='talaba')
    arizalar = Ariza.objects.all
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
    }
    return render(request, 'dekanatadmin/talaba_malumot.html', contex)


def talaba_tolov(request):    
    if request.method == 'POST':
        talaba_id = request.user.id
        narhi = request.POST['narhi']
        kivtansiya = request.FILES['kivtansiya']
        
        tolov = Tolov.objects.create(
            talaba_id=talaba_id, narhi = narhi, kivtansiya = kivtansiya
        )
        tolov.save()
        return redirect('/')
    
    contex = {
        
    }
    return render(request, 'talaba/tolov.html', contex)

def tolov_tasdiqlash(request, pk):
    tolov = Tolov.objects.get(id=pk)
   
    print(tolov.talaba_id)
    talaba = User.objects.filter(id=tolov.talaba_id)
    for t in talaba:
        ism  = t.first_name  
        print(ism)    
    data = get_object_or_404(Tolov, id=pk)                     
    data.tasdiqlash = 'tasdiqlandi'       
    data.save()
    
    contex = {
       'tolov':tolov, 
       'ism':ism,
    }
    return render(request, 'superadmin/tolov_tasdiqlash.html', contex)


def tolov_radetish(request, pk):
    tolov = Tolov.objects.get(id=pk)
   
    print(tolov.talaba_id)
    talaba = User.objects.filter(id=tolov.talaba_id)
    for t in talaba:
        ism  = t.first_name  
        print(ism)    
    data = get_object_or_404(Tolov, id=pk)                     
    data.tasdiqlash = 'radetildi'       
    data.save()
    
    contex = {
       'tolov':tolov, 
       'ism':ism,
    }
    return render(request, 'superadmin/tolov_tasdiqlash.html', contex)

def barcha_tolovlar(request):
    tolovlar = Tolov.objects.all()    
    contex = {
        'tolovlar': tolovlar,        
    }
    return render(request, 'superadmin/barcha_tolovlar.html', contex)

def tark_etish(request):
    talaba_id = request.user.id
    data = ''
    if request.method == 'POST':
        sabab = request.POST['sabab']
        if Tark_etgan.objects.filter(talaba_id=talaba_id):
            data = 'Oldin tark etib bolgansiz'
        else:
            data = Tark_etgan.objects.create(
                talaba_id=talaba_id, tark_etish='tark_etdi',
                sabab=sabab
            )
            data.save()
            return redirect('/')        
    
    contex = {
        'data':data,
    }
    return render(request, 'talaba/tark_etish.html', contex)

