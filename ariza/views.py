import csv
import qrcode
import xlwt
import datetime as dt
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from ariza.models import Ariza, Tolov, Tark_etgan, Barcha_tolov, Shartnoma, Order, Rasm, Imtiyoz, Order_link
from users.models import User


@csrf_exempt
def ariza(request):
    talaba_id = request.user.id
    first_name = request.user.first_name
    last_name = request.user.last_name
    sharif = request.user.sharif
    print(f'{first_name}  {last_name}  {sharif}')
    data = ''
    if request.method == 'POST':
        viloyat = request.POST['viloyat']
        tuman = request.POST['tuman']
        kocha = request.POST['kocha']
        fakultet = request.POST['fakultet']
        yonalish = request.POST['yonalish']  
        kurs = request.POST['kurs']
        pasport_serya = request.POST['pasport_serya']
        pasport_raqam = request.POST['pasport_raqam']
        pasport_rasm = request.FILES['pasport_rasm']       
        serya = f'{pasport_serya} {pasport_raqam}'
        print(serya)     
        
        if Ariza.objects.filter(pasport_serya_raqam=serya) or Ariza.objects.filter(talaba_id=talaba_id):
            data = 'Bu foydalanuvchi ariza yuborgan'
        else:
            ariza = Ariza.objects.create(
                talaba_id=talaba_id, first_name=first_name,
                last_name=last_name, sharif=sharif,
                viloyat = viloyat, tuman = tuman,
                kocha=kocha, fakultet = fakultet, yonalish=yonalish,
                kurs = kurs, pasport_serya_raqam=serya,
                pasport_rasm=pasport_rasm               
            ) 
            ariza.save()          
            return redirect('/ariza/ariza_imtiyoz/')   
    contex = {
        'data':data,
    }
    return render(request, 'talaba/ariza.html', contex)

@csrf_exempt
def arizalar(request):
    ariza_tasdiqlsh = Ariza.objects.filter(talaba_id=request.user.id).filter(tasdiqlash='tasdiqlandi')
    ariza_yuborish = Ariza.objects.filter(talaba_id=request.user.id)
    
    contex = {
        'ariza_tasdiqlsh':ariza_tasdiqlsh,
        'ariza_yuborish':ariza_yuborish,
    }
    return render(request, 'talaba/arizalar.html', contex)


@csrf_exempt
def ariza_imtiyoz(request):    
    ariza = Ariza.objects.filter(talaba_id=request.user.id)
    imtiyoz = Imtiyoz.objects.filter(talaba_id=request.user.id)
    if ariza:
        for a in ariza:
            familya = a.last_name
            ism = a.first_name
            ariza_holat = a.tasdiqlash
            ariza_xulosa = a.xulosa
            
    else:
        familya = ''
        ism = ''
        ariza_holat = ''
        ariza_xulosa = ''     
            
    if imtiyoz:
        for i in imtiyoz:
            imtiyoz_holat = i.tasdiqlash
            imtiyoz_xulosa = i.xulosa
    else:
        imtiyoz_holat = ''
        imtiyoz_xulosa = ''
        
    
    contex = {  
        'familya':familya,
        'ism':ism,      
        'ariza_holat':ariza_holat,
        'imtiyoz_holat':imtiyoz_holat,
        'ariza_xulosa':ariza_xulosa,
        'imtiyoz_xulosa':imtiyoz_xulosa,
        
                
    }
    return render(request, 'talaba/ariza_imtiyoz.html', contex)



# imtiyozlar bolimi uchun 
@csrf_exempt
def imtiyoz(request):
    talaba_id = request.user.id
    first_name = request.user.first_name
    last_name = request.user.last_name
    sharif = request.user.sharif
    data = ''
    if request.method == 'POST':       
        imtiyoz_nomi = request.POST['imtiyoz_nomi']
        imtiyoz_file = request.FILES['imtiyoz_file']   
        if imtiyoz_nomi == '':
            print('bosh')
        else:
            print('bosh emas')
            if Imtiyoz.objects.filter(talaba_id=talaba_id):
                data = 'Bu foydalanuvchi imtiyoz yuborgan'
            else:
                data = Imtiyoz.objects.create(
                    talaba_id=talaba_id, first_name= first_name,
                    last_name=last_name, sharif=sharif,
                    imtiyoz_nomi=imtiyoz_nomi, imtiyoz_file=imtiyoz_file,               
                ) 
                data.save()          
                return redirect('/ariza/ariza_imtiyoz/')   
    contex = {
        'data':data,
    }
    return render(request, 'talaba/imtiyoz.html', contex)





@csrf_exempt
def tolovlar(request, pk):
    data = Tolov.objects.filter(talaba_id=pk).filter(tasdiqlash='tasdiqlandi')

    if data:
        tolangan = 0
        for d in data:
            tolangan += int(d.narhi)
    else:
        tolangan = 0
    
    contex = {
        'tolangan':tolangan,
    }
    return render(request, 'talaba/tolovlar.html', contex)

#  superadmin arizalar
@csrf_exempt
def barcha_arizalar(request):
    talaba = User.objects.filter(lavozim='talaba')
    arizalar = Ariza.objects.filter(tasdiqlash='')   
    
    contex = {
        'talaba':talaba,
        'arizalar':arizalar,
    }
    return render(request, 'superadmin/barcha_arizalar.html', contex)


@csrf_exempt
def dekanat_barcha_arizalar(request):
    fakultet = request.user.fakultet 
    talaba = User.objects.filter(lavozim='talaba') 
    arizalar = Ariza.objects.filter(fakultet=fakultet).filter(tasdiqlash='') 
    
    contex = {
        'talaba':talaba,
        'arizalar':arizalar,
        'fakultet':fakultet,
    }
    return render(request, 'dekanatadmin/dekanat/dekanat_barcha_arizalar.html', contex)


@csrf_exempt
def dekanat_tasdiqlangan_arizalar(request):
    fakultet = request.user.fakultet
    talabalar = User.objects.filter(lavozim='talaba')
    data = Ariza.objects.filter(fakultet=fakultet).filter(tasdiqlash='tasdiqlandi')
    contex = {
        'data':data,
        'talabalar':talabalar,
    }
    return render(request,  'dekanatadmin/dekanat/dekanat_tasdiqlangan_arizalar.html', contex)


@csrf_exempt
def dekanat_radetilgan_arizalar(request):
    fakultet = request.user.fakultet
    talabalar = User.objects.filter(lavozim='talaba')
    data = Ariza.objects.filter(fakultet=fakultet).filter(tasdiqlash = 'radetildi')
    contex = {
        'data':data,
        'talabalar':talabalar,
    }
    return render(request,  'dekanatadmin/dekanat/dekanat_radetilgan_arizalar.html', contex)


@csrf_exempt
def dekanat_barcha_malumot(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.filter(talaba_id=pk)
    imtiyoz = Imtiyoz.objects.filter(talaba_id=pk)
    if talabalar:
        for t in talabalar:
            telefon = t.username
    else:
        telefon = ''
        
    if arizalar:
        for a in arizalar:
            rasm_url = a.pasport_rasm.url
            familya = a.last_name
            ism = a.first_name
            sharif = a.sharif
            pasport = a.pasport_serya_raqam
            fakultet = a.fakultet
            yonalish = a.yonalish
            kurs = a.kurs
            viloyat = a.viloyat
            tuman = a.tuman
            kocha = a.kocha
            
    else:
        rasm_url = 'Pasport rasmi joylanmagan'
        familya = ''
        ism = ''
        sharif = ''
        pasport = ''
        fakultet = ''
        yonalish = ''
        kurs = ''
        viloyat = ''
        tuman = ''
        kocha = ''
        
    if imtiyoz:  
        for i in imtiyoz:            
            imtiyoz_url = i.imtiyoz_file.url
            imtiyoz_turi = i.imtiyoz_nomi
    else:
        imtiyoz_url = 'Talabada imtiyoz mavjud emas'
        imtiyoz_turi = ''
        
    
    
    contex = {
        'talabalar':talabalar,'arizalar':arizalar,'imtiyoz':imtiyoz,'rasm_url':rasm_url,
        'imtiyoz_url':imtiyoz_url,'familya':familya,'ism':ism,'sharif':sharif,'telefon':telefon,
        'pasport':pasport,'imtiyoz_turi':imtiyoz_turi,'fakultet':fakultet,'yonalish':yonalish,
        'kurs':kurs,'viloyat':viloyat,'tuman':tuman,'kocha':kocha,
    }
    return render(request, 'dekanatadmin/dekanat/dekanat_barcha_malumot.html', contex)


@csrf_exempt
def dekanat_tasdiqlangan_malumot(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.filter(talaba_id=pk)
    imtiyoz = Imtiyoz.objects.filter(talaba_id=pk)
    if talabalar:
        for t in talabalar:
            telefon = t.username
    else:
        telefon = ''
        
    if arizalar:
        for a in arizalar:
            rasm_url = a.pasport_rasm.url
            familya = a.last_name
            ism = a.first_name
            sharif = a.sharif
            pasport = a.pasport_serya_raqam
            fakultet = a.fakultet
            yonalish = a.yonalish
            kurs = a.kurs
            viloyat = a.viloyat
            tuman = a.tuman
            kocha = a.kocha
            
    else:
        rasm_url = 'Pasport rasmi joylanmagan'
        familya = ''
        ism = ''
        sharif = ''
        pasport = ''
        fakultet = ''
        yonalish = ''
        kurs = ''
        viloyat = ''
        tuman = ''
        kocha = ''
        
    if imtiyoz:  
        for i in imtiyoz:            
            imtiyoz_url = i.imtiyoz_file.url
            imtiyoz_turi = i.imtiyoz_nomi
    else:
        imtiyoz_url = 'Talabada imtiyoz mavjud emas'
        imtiyoz_turi = ''
        
    
    
    contex = {
        'talabalar':talabalar,'arizalar':arizalar,'imtiyoz':imtiyoz,'rasm_url':rasm_url,
        'imtiyoz_url':imtiyoz_url,'familya':familya,'ism':ism,'sharif':sharif,'telefon':telefon,
        'pasport':pasport,'imtiyoz_turi':imtiyoz_turi,'fakultet':fakultet,'yonalish':yonalish,
        'kurs':kurs,'viloyat':viloyat,'tuman':tuman,'kocha':kocha,
    }
    return render(request, 'dekanatadmin/dekanat/dekanat_tasdiqlangan_malumot.html', contex)


@csrf_exempt
def dekanat_radetilgan_malumot(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.filter(talaba_id=pk)
    imtiyoz = Imtiyoz.objects.filter(talaba_id=pk)
    if talabalar:
        for t in talabalar:
            telefon = t.username
    else:
        telefon = ''
        
    if arizalar:
        for a in arizalar:
            rasm_url = a.pasport_rasm.url
            familya = a.last_name
            ism = a.first_name
            sharif = a.sharif
            pasport = a.pasport_serya_raqam
            fakultet = a.fakultet
            yonalish = a.yonalish
            kurs = a.kurs
            viloyat = a.viloyat
            tuman = a.tuman
            kocha = a.kocha
            
    else:
        rasm_url = 'Pasport rasmi joylanmagan'
        familya = ''
        ism = ''
        sharif = ''
        pasport = ''
        fakultet = ''
        yonalish = ''
        kurs = ''
        viloyat = ''
        tuman = ''
        kocha = ''
        
    if imtiyoz:  
        for i in imtiyoz:            
            imtiyoz_url = i.imtiyoz_file.url
            imtiyoz_turi = i.imtiyoz_nomi
    else:
        imtiyoz_url = 'Talabada imtiyoz mavjud emas'
        imtiyoz_turi = ''
        
    
    
    contex = {
        'talabalar':talabalar,'arizalar':arizalar,'imtiyoz':imtiyoz,'rasm_url':rasm_url,
        'imtiyoz_url':imtiyoz_url,'familya':familya,'ism':ism,'sharif':sharif,'telefon':telefon,
        'pasport':pasport,'imtiyoz_turi':imtiyoz_turi,'fakultet':fakultet,'yonalish':yonalish,
        'kurs':kurs,'viloyat':viloyat,'tuman':tuman,'kocha':kocha,
    }
    return render(request, 'dekanatadmin/dekanat/dekanat_radetilgan_malumot.html', contex)


@csrf_exempt
def arizalar_jadvali(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.filter(talaba_id=pk)
    imtiyoz = Imtiyoz.objects.filter(talaba_id=pk)
    if talabalar:
        for t in talabalar:
            telefon = t.username
    else:
        telefon = ''
        
    if arizalar:
        for a in arizalar:
            rasm_url = a.pasport_rasm.url
            familya = a.last_name
            ism = a.first_name
            sharif = a.sharif
            pasport = a.pasport_serya_raqam
            fakultet = a.fakultet
            yonalish = a.yonalish
            kurs = a.kurs
            viloyat = a.viloyat
            tuman = a.tuman
            kocha = a.kocha
            
    else:
        rasm_url = 'Pasport rasmi joylanmagan'
        familya = ''
        ism = ''
        sharif = ''
        pasport = ''
        fakultet = ''
        yonalish = ''
        kurs = ''
        viloyat = ''
        tuman = ''
        kocha = ''
        
    if imtiyoz:  
        for i in imtiyoz:            
            imtiyoz_url = i.imtiyoz_file.url
            imtiyoz_turi = i.imtiyoz_nomi
    else:
        imtiyoz_url = 'Talabada imtiyoz mavjud emas'
        imtiyoz_turi = ''
        
    
    
    contex = {
        'talabalar':talabalar,'arizalar':arizalar,'imtiyoz':imtiyoz,'rasm_url':rasm_url,
        'imtiyoz_url':imtiyoz_url,'familya':familya,'ism':ism,'sharif':sharif,'telefon':telefon,
        'pasport':pasport,'imtiyoz_turi':imtiyoz_turi,'fakultet':fakultet,'yonalish':yonalish,
        'kurs':kurs,'viloyat':viloyat,'tuman':tuman,'kocha':kocha,
    }
    return render(request, 'superadmin/arizalar_jadvali.html', contex)


# imtiyoz uchun
@csrf_exempt
def imtiyozli_arizalar(request):
    talabalar = User.objects.filter(lavozim='talaba')
    arizalar = Ariza.objects.filter(tasdiqlash='')
    imtiyozlar = Imtiyoz.objects.filter(tasdiqlash='')
    
    
    contex = {
        'talabalar':talabalar,
        'imtiyozlar':imtiyozlar,        
    }
    return render(request, 'superadmin/imtiyozli_arizalar.html', contex)


@csrf_exempt
def tasdiqlangan_imtiyozli_arizalar(request):
    talabalar = User.objects.filter(lavozim='talaba')
    imtiyozlar = Imtiyoz.objects.filter(tasdiqlash='tasdiqlandi')
    
    
    contex = {
        'talabalar':talabalar,
        'imtiyozlar':imtiyozlar,        
    }
    return render(request, 'superadmin/tasdiqlangan_imtiyozli_arizalar.html', contex)

@csrf_exempt
def imtiyoz_malumotlar(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.filter(talaba_id=pk)
    imtiyoz = Imtiyoz.objects.filter(talaba_id=pk)
    if talabalar:
        for t in talabalar:
            telefon = t.username
    else:
        telefon = ''
        
    if arizalar:
        for a in arizalar:
            rasm_url = a.pasport_rasm.url
            familya = a.last_name
            ism = a.first_name
            sharif = a.sharif
            pasport = a.pasport_serya_raqam
            fakultet = a.fakultet
            yonalish = a.yonalish
            kurs = a.kurs
            viloyat = a.viloyat
            tuman = a.tuman
            kocha = a.kocha
            
    else:
        rasm_url = 'Pasport rasmi joylanmagan'
        familya = ''
        ism = ''
        sharif = ''
        pasport = ''
        fakultet = ''
        yonalish = ''
        kurs = ''
        viloyat = ''
        tuman = ''
        kocha = ''
        
    if imtiyoz:  
        for i in imtiyoz:            
            imtiyoz_url = i.imtiyoz_file.url
            imtiyoz_turi = i.imtiyoz_nomi
    else:
        imtiyoz_url = 'Talabada imtiyoz mavjud emas'
        imtiyoz_turi = ''
        
    
    
    contex = {
        'talabalar':talabalar,'arizalar':arizalar,'imtiyoz':imtiyoz,'rasm_url':rasm_url,
        'imtiyoz_url':imtiyoz_url,'familya':familya,'ism':ism,'sharif':sharif,'telefon':telefon,
        'pasport':pasport,'imtiyoz_turi':imtiyoz_turi,'fakultet':fakultet,'yonalish':yonalish,
        'kurs':kurs,'viloyat':viloyat,'tuman':tuman,'kocha':kocha,
    }
    return render(request, 'superadmin/imtiyoz_malumotlar.html', contex)




@csrf_exempt
def tasdiqlangan_imtiyoz_malumotlar(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.filter(talaba_id=pk)
    imtiyoz = Imtiyoz.objects.filter(talaba_id=pk)
    if talabalar:
        for t in talabalar:
            telefon = t.username
    else:
        telefon = ''
        
    if arizalar:
        for a in arizalar:
            rasm_url = a.pasport_rasm.url
            familya = a.last_name
            ism = a.first_name
            sharif = a.sharif
            pasport = a.pasport_serya_raqam
            fakultet = a.fakultet
            yonalish = a.yonalish
            kurs = a.kurs
            viloyat = a.viloyat
            tuman = a.tuman
            kocha = a.kocha
            
    else:
        rasm_url = 'Pasport rasmi joylanmagan'
        familya = ''
        ism = ''
        sharif = ''
        pasport = ''
        fakultet = ''
        yonalish = ''
        kurs = ''
        viloyat = ''
        tuman = ''
        kocha = ''
        
    if imtiyoz:  
        for i in imtiyoz:            
            imtiyoz_url = i.imtiyoz_file.url
            imtiyoz_turi = i.imtiyoz_nomi
    else:
        imtiyoz_url = 'Talabada imtiyoz mavjud emas'
        imtiyoz_turi = ''
        
    
    
    contex = {
        'talabalar':talabalar,'arizalar':arizalar,'imtiyoz':imtiyoz,'rasm_url':rasm_url,
        'imtiyoz_url':imtiyoz_url,'familya':familya,'ism':ism,'sharif':sharif,'telefon':telefon,
        'pasport':pasport,'imtiyoz_turi':imtiyoz_turi,'fakultet':fakultet,'yonalish':yonalish,
        'kurs':kurs,'viloyat':viloyat,'tuman':tuman,'kocha':kocha,
    }
    return render(request, 'superadmin/tasdiqlangan_imtiyoz_malumot.html', contex)



@csrf_exempt
def imtiyozni_tasdiqlash(request, pk):
    talabalar = User.objects.get(id=pk)
    imtiyoz = Imtiyoz.objects.filter(talaba_id=pk)
    if request.method == 'POST':
        data = get_object_or_404(Imtiyoz, talaba_id=pk)
        xulosa = request.POST['xulosa']  
        data.xulosa = xulosa      
        data.tasdiqlash = 'tasdiqlandi'        
        data.save()
        return redirect('/ariza/imtiyozli_arizalar/')
    
    contex = {
        'talabalar':talabalar,
        'imtiyoz':imtiyoz,
    }
    return render(request, 'superadmin/imtiyozni_tasdiqlash.html', contex)


@csrf_exempt
def imtiyozni_radetish(request, pk):
    talabalar = User.objects.get(id=pk)
    imtiyoz = Imtiyoz.objects.filter(talaba_id=pk)
    if request.method == 'POST':
        data = get_object_or_404(Imtiyoz, talaba_id=pk)
        xulosa = request.POST['xulosa']  
        data.xulosa = xulosa      
        data.tasdiqlash = 'radetildi'        
        data.save()
        return redirect('/ariza/imtiyozli_arizalar/')
    contex = {
        'talabalar':talabalar,
        'imtiyoz':imtiyoz,
    }
    return render(request, 'superadmin/imtiyozni_radetish.html', contex)


@csrf_exempt
def dekanat_tasdiqlangan_ariza(request, pk):    
    talabalar = User.objects.get(id=pk)
    if request.method == 'POST':
        data = get_object_or_404(Ariza, talaba_id=pk)
        xulosa = request.POST['xulosa']  
        data.xulosa = xulosa      
        data.tasdiqlash = 'tasdiqlandi'        
        data.save()
        return redirect('/ariza/dekanat_barcha_arizalar/')
    contex = {
        'talabalar':talabalar,
    }
    return render(request, 'dekanatadmin/dekanat/tasdiqlangan_ariza.html', contex)



@csrf_exempt
def dekanat_radetilgan_ariza(request, pk):   
    talabalar = User.objects.get(id=pk)
    if request.method == 'POST':
        data = get_object_or_404(Ariza, talaba_id=pk)
        xulosa = request.POST['xulosa']  
        data.xulosa = xulosa      
        data.tasdiqlash = 'radetildi'        
        data.save()
        return redirect('/ariza/dekanat_barcha_arizalar/')
    contex = {
      'talabalar':talabalar,  
    }
    return render(request, 'dekanatadmin/dekanat/radetilgan_ariza.html', contex)


@csrf_exempt
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
    return render(request, 'superadmin/tasdiqlangan_ariza.html', contex)



@csrf_exempt
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
    return render(request, 'superadmin/radetilgan_ariza.html', contex)


@csrf_exempt
def tasdiqlangan(request):
    talabalar = User.objects.filter(lavozim='talaba')
    data = Ariza.objects.filter(tasdiqlash='tasdiqlandi')
    contex = {
        'data':data,
        'talabalar':talabalar,
    }
    return render(request,  'dekanatadmin/tasdiqlangan.html', contex)



@csrf_exempt
def radetilgan(request):
    talabalar = User.objects.filter(lavozim='talaba')
    data = Ariza.objects.filter(tasdiqlash = 'radetildi')
    contex = {
        'data':data,
        'talabalar':talabalar,
    }
    return render(request,  'dekanatadmin/radetilgan.html', contex)


@csrf_exempt
def talaba_malumotlar(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.all
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
    }
    return render(request, 'dekanatadmin/talaba_malumot.html', contex)


@csrf_exempt
def tasdiqlangan_malumotlar(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.filter(talaba_id=pk)
    imtiyoz = Imtiyoz.objects.filter(talaba_id=pk)
    if talabalar:
        for t in talabalar:
            telefon = t.username
    else:
        telefon = ''
        
    if arizalar:
        for a in arizalar:
            rasm_url = a.pasport_rasm.url
            familya = a.last_name
            ism = a.first_name
            sharif = a.sharif
            pasport = a.pasport_serya_raqam
            fakultet = a.fakultet
            yonalish = a.yonalish
            kurs = a.kurs
            viloyat = a.viloyat
            tuman = a.tuman
            kocha = a.kocha
            
    else:
        rasm_url = 'Pasport rasmi joylanmagan'
        familya = ''
        ism = ''
        sharif = ''
        pasport = ''
        fakultet = ''
        yonalish = ''
        kurs = ''
        viloyat = ''
        tuman = ''
        kocha = ''
        
    if imtiyoz:  
        for i in imtiyoz:            
            imtiyoz_url = i.imtiyoz_file.url
            imtiyoz_turi = i.imtiyoz_nomi
    else:
        imtiyoz_url = 'Talabada imtiyoz mavjud emas'
        imtiyoz_turi = ''
        
    
    
    contex = {
        'talabalar':talabalar,'arizalar':arizalar,'imtiyoz':imtiyoz,'rasm_url':rasm_url,
        'imtiyoz_url':imtiyoz_url,'familya':familya,'ism':ism,'sharif':sharif,'telefon':telefon,
        'pasport':pasport,'imtiyoz_turi':imtiyoz_turi,'fakultet':fakultet,'yonalish':yonalish,
        'kurs':kurs,'viloyat':viloyat,'tuman':tuman,'kocha':kocha,
    }
    return render(request, 'dekanatadmin/tasdiqlangan_malumot.html', contex)


@csrf_exempt
def radetilgan_malumotlar(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.filter(talaba_id=pk)
    imtiyoz = Imtiyoz.objects.filter(talaba_id=pk)
    if talabalar:
        for t in talabalar:
            telefon = t.username
    else:
        telefon = ''
        
    if arizalar:
        for a in arizalar:
            rasm_url = a.pasport_rasm.url
            familya = a.last_name
            ism = a.first_name
            sharif = a.sharif
            pasport = a.pasport_serya_raqam
            fakultet = a.fakultet
            yonalish = a.yonalish
            kurs = a.kurs
            viloyat = a.viloyat
            tuman = a.tuman
            kocha = a.kocha
            
    else:
        rasm_url = 'Pasport rasmi joylanmagan'
        familya = ''
        ism = ''
        sharif = ''
        pasport = ''
        fakultet = ''
        yonalish = ''
        kurs = ''
        viloyat = ''
        tuman = ''
        kocha = ''
        
    if imtiyoz:  
        for i in imtiyoz:            
            imtiyoz_url = i.imtiyoz_file.url
            imtiyoz_turi = i.imtiyoz_nomi
    else:
        imtiyoz_url = 'Talabada imtiyoz mavjud emas'
        imtiyoz_turi = ''
        
    
    
    contex = {
        'talabalar':talabalar,'arizalar':arizalar,'imtiyoz':imtiyoz,'rasm_url':rasm_url,
        'imtiyoz_url':imtiyoz_url,'familya':familya,'ism':ism,'sharif':sharif,'telefon':telefon,
        'pasport':pasport,'imtiyoz_turi':imtiyoz_turi,'fakultet':fakultet,'yonalish':yonalish,
        'kurs':kurs,'viloyat':viloyat,'tuman':tuman,'kocha':kocha,
    }
    return render(request, 'dekanatadmin/radetilgan_malumot.html', contex)



@csrf_exempt
def tark_etgan_malumotlar(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.filter(talaba_id=pk)
    imtiyozlar = Imtiyoz.objects.filter(talaba_id=pk)
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
        'imtiyozlar':imtiyozlar,
    }
    return render(request, 'dekanatadmin/tark_etgan_malumot.html', contex)

# talaba tolovlari haqida malumot dekanat uchun
@csrf_exempt
def talaba_tolov_malumotlar(request, pk):
    data_tolov = Tolov.objects.filter(id=pk)
    data = Tolov.objects.filter(id=pk)
    if data:
        for d in  data:
            talabalar = User.objects.filter(id=d.talaba_id)
            arizalar = Ariza.objects.filter(talaba_id=d.talaba_id)
            tarixlar = Tolov.objects.filter(talaba_id=d.talaba_id).filter(tasdiqlash='tasdiqlandi')
            narhi = d.narhi
            kivtansiya = d.kivtansiya             
            if tarixlar:
                for x in tarixlar:
                    narhi_t = x.narhi
                    kivtansiya_t = x.kivtansiya 
                    tasdiqlash = x.tasdiqlash
                    sana = x.sana
            else:
                narhi_t = ''
                kivtansiya_t = ''
                tasdiqlash = ''
                sana = ''
            if talabalar:
                for t in talabalar:
                    last_name = t.last_name
                    first_name = t.first_name
                    sharif = t.sharif
                    telefon = t.username
            else:
                last_name = ''
                first_name = ''
                sharif = ''
                telefon = ''            
            if arizalar:
                for a in arizalar:
                    pasport_serya_raqam = a.pasport_serya_raqam
                    fakultet = a.fakultet
                    yonalish = a.yonalish
                    kurs = a.kurs
                    viloyat = a.viloyat
                    tuman = a.tuman
                    kocha = a.kocha
            else:
                pasport_serya_raqam = ''
                fakultet = ''
                yonalish = ''
                kurs = ''
                viloyat = ''
                tuman = ''
                kocha = ''
  
        

    
    contex = {
        'data_tolov':data_tolov,
        'last_name':last_name,
        'first_name':first_name,
        'sharif':sharif,
        'telefon':telefon,
        'pasport_serya_raqam':pasport_serya_raqam,
        'fakultet':fakultet,
        'yonalish':yonalish,
        'kurs':kurs,
        'viloyat':viloyat,
        'tuman':tuman,
        'kocha':kocha,
        'narhi_t':narhi_t,
        'kivtansiya_t':kivtansiya_t,
        'tasdiqlash':tasdiqlash,
        'narhi':narhi,
        'kivtansiya':kivtansiya,
        'sana':sana,
        'tarixlar':tarixlar
    }
    return render(request, 'dekanatadmin/talaba_tolov_malumot.html', contex)


@csrf_exempt
def radetilgan_tolov_malumotlar(request, pk):
    data_tolov = Tolov.objects.filter(id=pk)
    data = Tolov.objects.filter(id=pk)
    if data:
        for d in  data:
            talabalar = User.objects.filter(id=d.talaba_id)
            arizalar = Ariza.objects.filter(talaba_id=d.talaba_id)
            tarixlar = Tolov.objects.filter(talaba_id=d.talaba_id).filter(tasdiqlash='tasdiqlandi')
            narhi = d.narhi
            kivtansiya = d.kivtansiya             
            if tarixlar:
                for x in tarixlar:
                    narhi_t = x.narhi
                    kivtansiya_t = x.kivtansiya 
                    tasdiqlash = x.tasdiqlash
                    sana = x.sana
            else:
                narhi_t = ''
                kivtansiya_t = ''
                tasdiqlash = ''
                sana = ''
            if talabalar:
                for t in talabalar:
                    last_name = t.last_name
                    first_name = t.first_name
                    sharif = t.sharif
                    telefon = t.username
            else:
                last_name = ''
                first_name = ''
                sharif = ''
                telefon = ''            
            if arizalar:
                for a in arizalar:
                    pasport_serya_raqam = a.pasport_serya_raqam
                    fakultet = a.fakultet
                    yonalish = a.yonalish
                    kurs = a.kurs
                    viloyat = a.viloyat
                    tuman = a.tuman
                    kocha = a.kocha
            else:
                pasport_serya_raqam = ''
                fakultet = ''
                yonalish = ''
                kurs = ''
                viloyat = ''
                tuman = ''
                kocha = ''
  
        

    
    contex = {
        'data_tolov':data_tolov,
        'last_name':last_name,
        'first_name':first_name,
        'sharif':sharif,
        'telefon':telefon,
        'pasport_serya_raqam':pasport_serya_raqam,
        'fakultet':fakultet,
        'yonalish':yonalish,
        'kurs':kurs,
        'viloyat':viloyat,
        'tuman':tuman,
        'kocha':kocha,
        'narhi_t':narhi_t,
        'kivtansiya_t':kivtansiya_t,
        'tasdiqlash':tasdiqlash,
        'narhi':narhi,
        'kivtansiya':kivtansiya,
        'sana':sana,
        'tarixlar':tarixlar
    }
    return render(request, 'dekanatadmin/radetilgan_tolov_malumotlar.html', contex)



@csrf_exempt
def talaba_tolov(request):  
    talaba_id = request.user.id
    first_name = request.user.first_name
    last_name = request.user.last_name
    sharif = request.user.sharif  
    if request.method == 'POST':        
        narhi = request.POST['narhi']
        kivtansiya = request.FILES['kivtansiya']
        
        if narhi == '':
            return redirect('/ariza/talaba_tolov/')
        else:        
            tolov = Tolov.objects.create(
                talaba_id=talaba_id, first_name=first_name,
                last_name=last_name, sharif=sharif,
                narhi = narhi, kivtansiya = kivtansiya
            )
            tolov.save()
            return redirect('/')
    
    contex = {
        
    }
    return render(request, 'talaba/tolov.html', contex)


@csrf_exempt
def tolov_tasdiqlash(request, pk):             
    data = get_object_or_404(Tolov, id=pk)                     
    data.tasdiqlash = 'tasdiqlandi'       
    data.save()
    
    return redirect('/ariza/barcha_tolovlar/')


@csrf_exempt
def tolov_radetish(request, pk):
    data = get_object_or_404(Tolov, id=pk)                     
    data.tasdiqlash = 'radetildi'       
    data.save()
    return redirect('/ariza/barcha_tolovlar/')
    
   
@csrf_exempt
def tasdiqlangan_tolov(request):
    talabalar = User.objects.filter(lavozim='talaba')
    tolovlar = Tolov.objects.filter(tasdiqlash='tasdiqlandi')
    arizalar = Ariza.objects.all()  
    
    contex = {
        'tolovlar': tolovlar, 
        'talabalar':talabalar, 
        'arizalar':arizalar,      
    }
    return render(request, 'superadmin/tasdiqlangan_tolov.html', contex)


@csrf_exempt
def superadminlar(request):
    data = User.objects.filter(lavozim='super')
    
    contex = {
        'data':data,
    }
    return render(request, 'superadmin/superadminlar.html', contex)


@csrf_exempt
def dekanatadminlar(request):
    data = User.objects.filter(lavozim='dekanat')
    
    contex = {
        'data':data,
    }
    return render(request, 'superadmin/dekanatadminlar.html', contex)


@csrf_exempt
def barcha_tolovlar(request):
    talabalar = User.objects.filter(lavozim='talaba')
    tolovlar = Tolov.objects.filter(tasdiqlash='')
    arizalar = Ariza.objects.all()  
    contex = {
        'tolovlar': tolovlar, 
        'talabalar':talabalar, 
        'arizalar':arizalar,      
    }
    return render(request, 'superadmin/barcha_tolovlar.html', contex)


@csrf_exempt
def tark_etish(request):
    talaba_id = request.user.id
    first_name = request.user.first_name
    last_name = request.user.last_name
    sharif = request.user.sharif 
    data = ''
    if request.method == 'POST':
        sabab = request.POST['sabab']
        if Tark_etgan.objects.filter(talaba_id=talaba_id):
            data = 'Oldin tark etib bolgansiz'
        else:
            data = Tark_etgan.objects.create(
                talaba_id=talaba_id, first_name=first_name,
                last_name=last_name, sharif=sharif,
                tark_etish='tark_etdi',
                sabab=sabab
            )
            data.save()
            return redirect('/')        
    
    contex = {
        'data':data,
    }
    return render(request, 'talaba/tark_etish.html', contex)



@csrf_exempt
def tark_etgan_talaba(request):
    talabalar = User.objects.filter(lavozim='talaba')
    data = Tark_etgan.objects.filter(tark_etish='tark_etdi')
    
    contex = {
        'data':data,
        'talabalar':talabalar,
    }
    return render(request, 'superadmin/tark_etgan_talaba.html', contex)


@csrf_exempt
def hisob_varoq(request):
    tolov_id = Barcha_tolov.objects.filter(kiritish = 'kiritildi')
    if request.method == 'POST': 
        boshlanginch_tolov = request.POST['boshlanginch_tolov']       
        oylik = request.POST['oylik']
        yillik_tolov = request.POST['yillik_tolov']        
        ttj_soni = request.POST['ttj_soni']
        xonalar_soni = request.POST['xonalar_soni']
        if tolov_id:
            for t in tolov_id:
                data = get_object_or_404(Barcha_tolov, id=t.id)
                data.boshlanginch_tolov = boshlanginch_tolov
                data.oylik = oylik
                data.yillik_tolov = yillik_tolov
                data.ttj_soni = ttj_soni
                data.xonalar_soni = xonalar_soni
                data.save()
                return redirect('/')
        else:        
            data = Barcha_tolov.objects.create(
                kiritish = 'kiritildi',yillik_tolov=yillik_tolov,
                boshlanginch_tolov=boshlanginch_tolov, oylik=oylik,
                ttj_soni=ttj_soni, xonalar_soni=xonalar_soni,
            )
            data.save()
            return redirect('/')
    
    contex = {
        
    }
    return render(request, 'superadmin/hisob_varoq.html', contex)


@csrf_exempt
def tolov_chek(request):
    talaba_id = request.user.id
    arizalar = Ariza.objects.filter(talaba_id=talaba_id)
    for a in arizalar:
        familya = a.last_name
        ism = a.first_name
        sharif = a.sharif
        fakultet = a.fakultet
        yonalish = a.yonalish
        kurs = a.kurs
    
    contex = {
        'familya':familya,
        'ism':ism,
        'sharif':sharif,
        'fakultet':fakultet,
        'yonalish':yonalish,
        'kurs':kurs,
    }
    
    template_path = 'talaba/tolov_chek.html' 
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # korib keyin saqlab olish
    response['Content-Disposition'] = 'filename="shartnoma.pdf"'
#     avto saqlab olish
#     response['Content-Disposition'] = 'attachment; filename="report.pdf"


    # find the template and render it.
    template = get_template(template_path)
    
    html = template.render(contex)
    
    

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse("Bizda ba'zi xatolar bor edi " + html + " serverda texnik ish lar olib borilmoqda !!!")
   
      
    return response


@csrf_exempt
def shartnomalar(request): 
    talaba = User.objects.filter(id=request.user.id)
    tasdiqlangan_tolov = Tolov.objects.filter(talaba_id=request.user.id).filter(tasdiqlash='tasdiqlandi')
    tasdiqlangan_orderlar = Order.objects.filter(talaba_id=request.user.id).filter(tasdiqlash='tasdiqlandi')
    
    contex = {  
        'talaba':talaba,
        'tasdiqlangan_tolov':tasdiqlangan_tolov, 
        'tasdiqlangan_orderlar':tasdiqlangan_orderlar,          
    }  
    return render(request, 'talaba/shartnomalar.html', contex)


@csrf_exempt
def shartnoma(request, pk):
    talaba_id = User.objects.filter(id=pk)    
    arizalar = Ariza.objects.filter(tasdiqlash='tasdiqlandi').filter(talaba_id=pk)
    if arizalar:        
        for a in arizalar:
            shartnoma = Shartnoma.objects.filter(talaba_id=pk)               
            if shartnoma:                   
                    # update qilish
                    talaba_f_i_sh = f'{a.last_name} {a.first_name} {a.sharif}'
                    manzil = f'{a.viloyat} {a.tuman} {a.kocha}'
                    iib_manzil = f'{a.viloyat} {a.tuman}'
                    data = get_object_or_404(Shartnoma, talaba_id=pk)
                    data.talaba_f_i_sh = talaba_f_i_sh
                    data.manzil = manzil
                    data.iib_manzil = iib_manzil
                    data.pasport = a.pasport_serya_raqam
                    data.save()
                    print('update qilindi')
            else:
                    talaba_f_i_sh = f'{a.last_name} {a.first_name} {a.sharif}'
                    manzil = f'{a.viloyat} {a.tuman} {a.kocha}'
                    iib_manzil = f'{a.viloyat} {a.tuman}'
                    ttj_nomer = ''
                    data = Shartnoma.objects.create(
                        talaba_id = pk,
                        talaba_f_i_sh = talaba_f_i_sh,
                        manzil = manzil,
                        iib_manzil = iib_manzil,
                        pasport = a.pasport_serya_raqam,
                        ttj_nomer=ttj_nomer
                    )
                    data.save()
                    print('yangi kiritildi')


    else:
        arizalar = 'Hozirda ariza mavjud emas'

    for t in talaba_id:
        import qrcode
        import datetime as dt


        data = f"https://ttj.kspi.uz/ariza/shartnoma/{pk}/"  # QR-kodga kiritmoqchi bo'lgan ma'lumot

        # QR-kod obyektini yaratish
        qr = qrcode.QRCode(version=1, box_size=10, border=4)

        # Ma'lumotni QR-kodga qo'shish
        qr.add_data(data)

        # QR-kodni yaratish
        qr.make()

        # QR-koddan tasvir yaratish
        img = qr.make_image()

        # Tasvirni saqlash
        img.save(f"media/code/qrcode{pk}.png")
        
        link = f'http://ttj.kspi.uz/media/code/qrcode{pk}.png'
        rasmlar = Rasm.objects.filter(talaba_id=pk)
        qrcode = Rasm.objects.filter(talaba_id=pk)
        
        
        media_url = '/code/'
        image_path = f'qrcode{pk}.png'
        image_url = f'{media_url}{image_path}'
        if rasmlar:
            data = get_object_or_404(Rasm, talaba_id=pk)
            data.talaba_id = pk
            data.link = link 
            data.rasm = image_url
            data.save()
            print('update qilindi')
        else:
            data = Rasm.objects.create(
                talaba_id = pk,
                link = link,
                rasm = image_url
            )
            data.save()
            print('create qilindi')
    
   
    talaba = User.objects.filter(id=pk)     
    hozir = dt.datetime.now()
    yil = hozir.year
    oy = hozir.month
    kun = hozir.day
    shartnoma = Shartnoma.objects.filter(talaba_id=pk)
    qrcode_rasm = Rasm.objects.filter(talaba_id=pk)

    
    contex = {        
        'yil':yil,
        'arizalar':arizalar,
        'oy':oy,
        'kun':kun,
        'hozir':hozir,
        'qrcode_rasm':qrcode_rasm,   
        'talaba':talaba,
        'shartnoma':shartnoma,           
    }  
    
    
    
    
    template_path = 'talaba/shartnoma.html' 
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # korib keyin saqlab olish
    response['Content-Disposition'] = 'filename="shartnoma.pdf"'
#     avto saqlab olish
#     response['Content-Disposition'] = 'attachment; filename="report.pdf"


    # find the template and render it.
    template = get_template(template_path)
    
    html = template.render(contex)
    
    

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse("Bizda ba'zi xatolar bor edi " + html + " serverda texnik ish lar olib borilmoqda !!!")
   
      
    return response


@csrf_exempt
def order(request, pk):
    import qrcode    
    order = Order.objects.filter(talaba_id=pk)     
    data = f"https://ttj.kspi.uz/ariza/order/{pk}/"  # QR-kodga kiritmoqchi bo'lgan ma'lumot

    # QR-kod obyektini yaratish
    qr = qrcode.QRCode(version=1, box_size=10, border=4)

    # Ma'lumotni QR-kodga qo'shish
    qr.add_data(data)

     # QR-kodni yaratish
    qr.make()

    # QR-koddan tasvir yaratish
    img = qr.make_image()

    # Tasvirni saqlash
    img.save(f"media/order_qrcode/qrcode{pk}.png")
        
    link = f'http://ttj.kspi.uz/media/order_qrcode/qrcode{pk}.png'
    rasmlar = Order_link.objects.filter(talaba_id=pk)
    qrcode = Order_link.objects.filter(talaba_id=pk)
        
        
    media_url = '/order_qrcode/'
    image_path = f'qrcode{pk}.png'
    image_url = f'{media_url}{image_path}'
    if rasmlar:
        data = get_object_or_404(Order_link, talaba_id=pk)
        data.talaba_id = pk
        data.link = link 
        data.rasm = image_url
        data.save()
        print('update qilindi')
    else:
            data = Order_link.objects.create(
                talaba_id = pk,
                link = link,
                rasm = image_url
            )
            data.save()
            print('create qilindi')
        
    
   
    talaba = User.objects.filter(id=pk)     
    hozir = dt.datetime.now()    
    qrcode_rasm = Order_link.objects.filter(talaba_id=pk)
    if order:
        for o in order:
            familya = o.familiya
            ism = o.ism
            sharif = o.sharif
            fakultet = o.fakultet
            yonalish = o.yonalish
            kurs = o.kurs
            manzil= o.manzil
            ttj_nomer = o.ttj_nomer
            ttj_manzil = o.ttj_manzil
            qavat = o.qavat
            xona = o.xona
            order_id = o.id
    else:
        familya = ''
        ism = ''
        sharif = ''
        fakultet = ''
        yonalish = ''
        kurs = ''
        manzil = ''
        ttj_nomer = ''
        ttj_manzil = ''
        qavat = ''
        xona = ''
        order_id = ''
            
    contex = {
        'ariza':ariza,
        'familya':familya,
        'ism':ism,
        'sharif':sharif,
        'fakultet':fakultet,
        'yonalish':yonalish,
        'kurs':kurs,
        'manzil':manzil,
        'ttj_nomer':ttj_nomer,
        'ttj_manzil':ttj_manzil,
        'qavat':qavat,
        'xona':xona,
        'hozir':hozir,
        'qrcode_rasm':qrcode_rasm,   
        'talaba':talaba,
        'order_id':order_id,                   
    }  
    
    
    
    
    template_path = 'talaba/order.html' 
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # korib keyin saqlab olish
    response['Content-Disposition'] = 'filename="order.pdf"'
#     avto saqlab olish
#     response['Content-Disposition'] = 'attachment; filename="report.pdf"


    # find the template and render it.
    template = get_template(template_path)
    
    html = template.render(contex)
    
    

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse("Bizda ba'zi xatolar bor edi " + html + " serverda texnik ish lar olib borilmoqda !!!")
   
      
    return response


def order_berish(request, pk):
    order_id = Order.objects.filter(talaba_id=pk)
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.filter(talaba_id=pk).filter(tasdiqlash='tasdiqlandi')
    imtiyoz = Imtiyoz.objects.filter(talaba_id=pk).filter(tasdiqlash='tasdiqlandi')
    tarixlar = Tolov.objects.filter(talaba_id=pk).filter(tasdiqlash='tasdiqlandi')
    if talabalar:
        for t in talabalar:
            telefon = t.username
    else:
        telefon = ''
        
    if arizalar:
        for a in arizalar:
            rasm_url = a.pasport_rasm.url
            familya = a.last_name
            ism = a.first_name
            sharif = a.sharif
            pasport = a.pasport_serya_raqam
            fakultet = a.fakultet
            yonalish = a.yonalish
            kurs = a.kurs
            viloyat = a.viloyat
            tuman = a.tuman
            kocha = a.kocha
            
    else:
        rasm_url = 'Pasport rasmi joylanmagan'
        familya = ''
        ism = ''
        sharif = ''
        pasport = ''
        fakultet = ''
        yonalish = ''
        kurs = ''
        viloyat = ''
        tuman = ''
        kocha = ''
        
    if imtiyoz:  
        for i in imtiyoz:            
            imtiyoz_url = i.imtiyoz_file.url
            imtiyoz_turi = i.imtiyoz_nomi
    else:
        imtiyoz_url = 'Talabada imtiyoz mavjud emas'
        imtiyoz_turi = ''  
    
    
    if request.method == 'POST': 
        ttj_manzil = request.POST['ttj_manzil']   
        ttj_nomer = request.POST['ttj_nomer']       
        qavat = request.POST['qavat']
        xona = request.POST['xona']        
        
        if order_id:
            for t in order_id:
                data = get_object_or_404(Order, talaba_id=pk)
                data.ttj_manzil = ttj_manzil
                data.ttj_nomer = ttj_nomer
                data.qavat = qavat
                data.xona = xona 
                data.telefon = telefon
                data.imtiyoz_nomi = imtiyoz_turi
                data.tasdiqlash='tasdiqlandi'               
                data.save()
                return redirect('/ariza/barcha_orderlar/')
        else:        
            data = Order.objects.create(
                ttj_manzil=ttj_manzil,ttj_nomer=ttj_nomer,
                qavat=qavat,xona=xona,
                telefon=telefon,imtiyoz_nomi=imtiyoz_turi,
                tasdiqlash='tasdiqlandi',                
            )
            data.save()
            return redirect('/ariza/barcha_orderlar/')
    
    contex = {
        'talabalar':talabalar,'arizalar':arizalar,'imtiyoz':imtiyoz,'rasm_url':rasm_url,
        'imtiyoz_url':imtiyoz_url,'familya':familya,'ism':ism,'sharif':sharif,'telefon':telefon,
        'pasport':pasport,'imtiyoz_turi':imtiyoz_turi,'fakultet':fakultet,'yonalish':yonalish,
        'kurs':kurs,'viloyat':viloyat,'tuman':tuman,'kocha':kocha, 'tarixlar':tarixlar
    }
    return render(request, 'superadmin/order_berish.html', contex)


def barcha_orderlar(request):
    arizalar = Ariza.objects.filter(tasdiqlash='tasdiqlandi') 
    rad = Ariza.objects.filter(tasdiqlash='radetildi')
    orderlar = Order.objects.filter(tasdiqlash='') 
               
    if arizalar:        
        for a in arizalar:
            manzil = f'{a.viloyat} {a.tuman}'
            order = Order.objects.filter(talaba_id=a.talaba_id)
            if order: 
                for o in order:       
                    data = get_object_or_404(Order, id=o.id)
                    data.familiya=a.last_name
                    data.ism=a.first_name
                    data.sharif=a.sharif
                    data.fakultet=a.fakultet
                    data.yonalish=a.yonalish
                    data.kurs=a.kurs
                    data.manzil=manzil
                    data.viloyat=a.viloyat
                    data.tuman=a.tuman
                    data.kocha=a.kocha                               
                           
            else:
                data = Order.objects.create(
                    talaba_id=a.talaba_id,familiya=a.last_name,ism=a.first_name,
                    sharif=a.sharif,fakultet=a.fakultet,yonalish=a.yonalish,
                    kurs=a.kurs,manzil=manzil,viloyat=a.viloyat,tuman=a.tuman,
                    kocha=a.kocha
                )
                data.save()               
                
                
    else:
        arizalar = '' 

    if rad:
        for r in rad:
            data = Order.objects.filter(talaba_id=r.talaba_id)
            data.delete()  
  
        
    
    contex = {
       'arizalar':arizalar,
       'orderlar':orderlar,       
    }
    return render(request, 'superadmin/barcha_orderlar.html', contex)



@csrf_exempt
def order_csv(request):
    # content-type of response
        response = HttpResponse(content_type='application/ms-excel')

        #decide file name
        response['Content-Disposition'] = 'attachment; filename="arizalar.xls"'

        #creating workbook
        wb = xlwt.Workbook(encoding='utf-8')

        #adding sheet
        ws = wb.add_sheet("sheet1")

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        # headers are bold
        font_style.font.bold = True

        #column header names, you can use your own headers here
        columns = [
            'TTJ nomer',
            'Qavat', 
            'Xona',
            'Jins',
            'Xona holati',
            'Fakultet',
            'Yonalish',
            'Kurs',
            'Talaba FISH',
            'Joylashtirilgan sana',  
            'Tark etgan sana',
            'Viloyat',
            'Tuman',
            'Ko`cha',
            'Order raqami',
            'Shartnoma raqami',
            'Talaba telefon raqami', 
            'Tolovi',
            'Oylik tolov summasi',
            'Tolov amalga oshirilgan sana',
            'Tolovning tugash sanasi',
            'Qarizdorlik',
            'Qaytarilgan mablag`',
            'Imtiyoz holati'                        
        ]

        #write column headers in sheet
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        #get your data, from database or from a text file...
        orderlar  = Order.objects.filter(tasdiqlash='tasdiqlandi')
        if orderlar:
            for my_row in orderlar:  
                talaba_fish = f'{my_row.familiya} {my_row.ism} {my_row.sharif}'              
                row_num = row_num + 1
                ws.write(row_num, 0, my_row.ttj_nomer, font_style)
                ws.write(row_num, 1, my_row.qavat, font_style)
                ws.write(row_num, 2, my_row.xona, font_style)
                ws.write(row_num, 3, '', font_style)
                ws.write(row_num, 4, '', font_style)
                ws.write(row_num, 5, my_row.fakultet, font_style)
                ws.write(row_num, 6, my_row.yonalish, font_style)
                ws.write(row_num, 7, my_row.kurs, font_style)
                ws.write(row_num, 8, talaba_fish, font_style)
                ws.write(row_num, 9, '', font_style)
                ws.write(row_num, 10, '', font_style)
                ws.write(row_num, 11, my_row.viloyat, font_style)
                ws.write(row_num, 12, my_row.tuman, font_style)
                ws.write(row_num, 13, my_row.kocha, font_style)
                ws.write(row_num, 14, my_row.id, font_style)
                ws.write(row_num, 15, my_row.id, font_style)
                ws.write(row_num, 16, my_row.telefon, font_style)
                ws.write(row_num, 17, '', font_style)
                ws.write(row_num, 18, '', font_style)
                ws.write(row_num, 19, '', font_style)
                ws.write(row_num, 20, '', font_style)
                ws.write(row_num, 21, '', font_style)
                ws.write(row_num, 22, '', font_style)
                ws.write(row_num, 23, my_row.imtiyoz_nomi, font_style)    
                

            wb.save(response)
            return response
        else:
            return redirect('/ariza/barcha_orderlar/')
        


@csrf_exempt
def ariza_csv(request):        
        # content-type of response
        response = HttpResponse(content_type='application/ms-excel')

        #decide file name
        response['Content-Disposition'] = 'attachment; filename="arizalar.xls"'

        #creating workbook
        wb = xlwt.Workbook(encoding='utf-8')

        #adding sheet
        ws = wb.add_sheet("sheet1")

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        # headers are bold
        font_style.font.bold = True

        #column header names, you can use your own headers here
        columns = [
            'Familya', 
            'Ism', 
            'Sharif', 
            'Viloyat', 
            'Tuman', 
            'Ko`cha', 
            'Fakultet', 
            'Yonalish',
            'Kurs',
            'Paspor serya raqam',                               
        ]

        #write column headers in sheet
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        #get your data, from database or from a text file...
        arizalar = Ariza.objects.filter(tasdiqlash='tasdiqlandi')
        if arizalar:
            for my_row in arizalar:                
                row_num = row_num + 1
                ws.write(row_num, 0, my_row.last_name, font_style)
                ws.write(row_num, 1, my_row.first_name, font_style)
                ws.write(row_num, 2, my_row.sharif, font_style)
                ws.write(row_num, 3, my_row.viloyat, font_style)
                ws.write(row_num, 4, my_row.tuman, font_style)
                ws.write(row_num, 5, my_row.kocha, font_style)
                ws.write(row_num, 6, my_row.fakultet, font_style)
                ws.write(row_num, 7, my_row.yonalish, font_style)
                ws.write(row_num, 8, my_row.kurs, font_style)
                ws.write(row_num, 9, my_row.pasport_serya_raqam, font_style)
                    

            wb.save(response)
            return response
        else:
            return redirect('/ariza/tasdiqlangan/')
        

@csrf_exempt
def tolov_csv(request):        
        # content-type of response
        response = HttpResponse(content_type='application/ms-excel')

        #decide file name
        response['Content-Disposition'] = 'attachment; filename="tolovlar.xls"'

        #creating workbook
        wb = xlwt.Workbook(encoding='utf-8')

        #adding sheet
        ws = wb.add_sheet("sheet1")

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        # headers are bold
        font_style.font.bold = True

        #column header names, you can use your own headers here
        columns = [
            'Familya', 
            'Ism', 
            'Sharif', 
            'Narhi', 
            'Sana',                                          
        ]

        #write column headers in sheet
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        #get your data, from database or from a text file...
        tolovlar = Tolov.objects.filter(tasdiqlash='tasdiqlandi')
        if tolovlar:
            for my_row in tolovlar:                
                row_num = row_num + 1
                vaqt = f'{my_row.sana}'
                ws.write(row_num, 0, my_row.last_name, font_style)
                ws.write(row_num, 1, my_row.first_name, font_style)
                ws.write(row_num, 2, my_row.sharif, font_style)
                ws.write(row_num, 3, my_row.narhi, font_style)
                ws.write(row_num, 4, vaqt[:16], font_style)
                                    

            wb.save(response)
            return response
        else:
            return redirect('/ariza/tasdiqlangan_tolov/')