from django.shortcuts import render, redirect
from ariza.models import Ariza, Imtiyoz


def arizalar(request):
    talaba_id = request.user.id
    data = 'ariza toldirish uchun'
    if request.method == 'POST':
        viloyat = request.POST['viloyat']
        tuman = request.POST['tuman']
        fakultet = request.POST['fakultet']
        yonalish = request.POST['yonalish']  
        kurs = request.POST['kurs']
        pasport_rasm = request.FILES['pasport_rasm']
        nogironlig = request.POST['nogironlig']       
        chin_yetim = request.POST['chin_yetim']             
        daftar_turishi = request.POST['daftar_turishi']        
        boquvchisini_yoqotgan = request.POST['boquvchisini_yoqotgan']
        
        
        ariza = Ariza.objects.create(
                talaba_id=talaba_id, viloyat = viloyat, tuman = tuman, 
                fakultet = fakultet, yonalish=yonalish,
                kurs = kurs, pasport_rasm=pasport_rasm,
                nogironlig=nogironlig, 
                chin_yetim=chin_yetim,
                daftar_turishi=daftar_turishi, 
                boquvchisini_yoqotgan=boquvchisini_yoqotgan,
        ) 
        ariza.save()          
        return redirect('/')  
    print(talaba_id)
    contex = {
        'data':data,
    }
    return render(request, 'talaba/arizalar.html', contex)

def imtiyozlar(request):
    if request.method == 'POST':
        talaba_id = request.user.id
        nomi = request.POST['nomi']
        file = request.FILES['file']
        
        imtiyoz = Imtiyoz.objects.create(
           talaba_id = talaba_id, nomi = nomi, file = file, 
        )
        imtiyoz.save()
        return redirect('/')
    contex = {
        
    }
    return render(request, 'talaba/imtiyozlar.html', contex)