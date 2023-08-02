import csv
import qrcode
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
    
    contex = {
        'ariza_tasdiqlsh':ariza_tasdiqlsh,
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
    data = Tolov.objects.filter(talaba_id=pk)
    
    contex = {
        'data':data,
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
    talaba = User.objects.filter(lavozim='talaba')
    arizalar = Ariza.objects.all()  
    fakultet = request.user.fakultet 
    
    contex = {
        'talaba':talaba,
        'arizalar':arizalar,
        'fakultet':fakultet,
    }
    return render(request, 'dekanatadmin/dekanat/dekanat_barcha_arizalar.html', contex)


@csrf_exempt
def dekanat_tasdiqlangan_arizalar(request):
    talabalar = User.objects.filter(lavozim='talaba')
    data = Ariza.objects.filter(tasdiqlash='tasdiqlandi')
    contex = {
        'data':data,
        'talabalar':talabalar,
    }
    return render(request,  'dekanatadmin/dekanat/dekanat_tasdiqlangan_arizalar.html', contex)


@csrf_exempt
def dekanat_radetilgan_arizalar(request):
    talabalar = User.objects.filter(lavozim='talaba')
    data = Ariza.objects.filter(tasdiqlash = 'radetildi')
    contex = {
        'data':data,
        'talabalar':talabalar,
    }
    return render(request,  'dekanatadmin/dekanat/dekanat_radetilgan_arizalar.html', contex)


@csrf_exempt
def dekanat_barcha_malumot(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.filter(talaba_id=request.user.pk)
    imtiyozlar = Imtiyoz.objects.filter(talaba_id=pk)
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
        'imtiyozlar':imtiyozlar,
    }
    return render(request, 'dekanatadmin/dekanat/dekanat_barcha_malumot.html', contex)


@csrf_exempt
def dekanat_tasdiqlangan_malumot(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.filter(talaba_id=pk)
    imtiyozlar = Imtiyoz.objects.filter(talaba_id=pk)
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
        'imtiyozlar':imtiyozlar,
    }
    return render(request, 'dekanatadmin/dekanat/dekanat_tasdiqlangan_malumot.html', contex)


@csrf_exempt
def dekanat_radetilgan_malumot(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.filter(talaba_id=pk)
    imtiyozlar = Imtiyoz.objects.filter(talaba_id=pk)
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
        'imtiyozlar':imtiyozlar,
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
    return render(request, 'dekanatadmin/radetilgan_ariza.html', contex)


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
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.filter(talaba_id=pk)
    tolovlar = Tolov.objects.filter(talaba_id=pk)
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
        'tolovlar':tolovlar,
    }
    return render(request, 'dekanatadmin/talaba_tolov_malumot.html', contex)


@csrf_exempt
def radetilgan_tolov_malumotlar(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.filter(talaba_id=pk)
    tolovlar = Tolov.objects.filter(talaba_id=pk)
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
        'tolovlar':tolovlar,
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
             
    data = get_object_or_404(Tolov, talaba_id=pk)                     
    data.tasdiqlash = 'tasdiqlandi'       
    data.save()
    
    return redirect('/ariza/barcha_tolovlar/')


@csrf_exempt
def tolov_radetish(request, pk):             
    data = get_object_or_404(Tolov, talaba_id=pk)                     
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
    talaba_id = User.objects.all()
    for t in talaba_id:
        arizalar = Ariza.objects.filter(talaba_id=t.id)
        if arizalar:
            for a in arizalar:
                shartnoma = Shartnoma.objects.filter(talaba_id=t.id)               
                if shartnoma:
                    # update qilish
                    talaba_f_i_sh = f'{a.last_name} {a.first_name} {a.sharif}'
                    manzil = f'{a.viloyat} {a.tuman} {a.kocha}'
                    iib_manzil = f'{a.viloyat} {a.tuman}'
                    data = get_object_or_404(Shartnoma, talaba_id=t.id)
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
                        talaba_id = t.id,
                        talaba_f_i_sh = talaba_f_i_sh,
                        manzil = manzil,
                        iib_manzil = iib_manzil,
                        pasport = a.pasport_serya_raqam,
                        ttj_nomer=ttj_nomer
                    )
                    data.save()
                    print('yangi kiritildi')


        else:
            ariza = 'Hozirda ariza mavjud emas'

    for t in talaba_id:
        import qrcode
        import datetime as dt


        data = f"https://ttj.kspi.uz/ariza/shartnomalar/{t.id}/"  # QR-kodga kiritmoqchi bo'lgan ma'lumot

        # QR-kod obyektini yaratish
        qr = qrcode.QRCode(version=1, box_size=10, border=4)

        # Ma'lumotni QR-kodga qo'shish
        qr.add_data(data)

        # QR-kodni yaratish
        qr.make()

        # QR-koddan tasvir yaratish
        img = qr.make_image()

        # Tasvirni saqlash
        img.save(f"media/code/qrcode{t.id}.png")
        
        link = f'http://ttj.kspi.uz/media/code/qrcode{t.id}.png'
        rasmlar = Rasm.objects.filter(talaba_id=t.id)
        qrcode = Rasm.objects.filter(talaba_id=t.id)
        
        
        media_url = '/code/'
        image_path = f'qrcode{t.id}.png'
        image_url = f'{media_url}{image_path}'
        if rasmlar:
            data = get_object_or_404(Rasm, talaba_id=t.id)
            data.talaba_id = t.id
            data.link = link 
            data.rasm = image_url
            data.save()
            print('update qilindi')
        else:
            data = Rasm.objects.create(
                talaba_id = t.id,
                link = link,
                rasm = image_url
            )
            data.save()
            print('create qilindi')
    
   
    talaba = User.objects.filter(id=request.user.id)     
    hozir = dt.datetime.now()
    yil = hozir.year
    oy = hozir.month
    kun = hozir.day
    tasdiqlangan_tolov = Tolov.objects.filter(talaba_id=request.user.id).filter(tasdiqlash='tasdiqlandi')
    tasdiqlangan_orderlar = Order.objects.filter(talaba_id=request.user.id).filter(tasdiqlash='tasdiqlandi')
    
    contex = {        
        'yil':yil,
        'ariza':ariza,
        'oy':oy,
        'kun':kun,
        'hozir':hozir,
        'qrcode':qrcode,   
        'talaba':talaba,
        'tasdiqlangan_tolov':tasdiqlangan_tolov, 
        'tasdiqlangan_orderlar':tasdiqlangan_orderlar,          
    }  
    return render(request, 'talaba/shartnomalar.html', contex)


@csrf_exempt
def shartnoma(request, pk):
    talaba_id = User.objects.all()
    for t in talaba_id:
        arizalar = Ariza.objects.filter(talaba_id=t.id)
        if arizalar:
            for a in arizalar:
                shartnoma = Shartnoma.objects.filter(talaba_id=t.id)               
                if shartnoma:
                    # update qilish
                    talaba_f_i_sh = f'{a.last_name} {a.first_name} {a.sharif}'
                    manzil = f'{a.viloyat} {a.tuman} {a.kocha}'
                    iib_manzil = f'{a.viloyat} {a.tuman}'
                    data = get_object_or_404(Shartnoma, talaba_id=t.id)
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
                        talaba_id = t.id,
                        talaba_f_i_sh = talaba_f_i_sh,
                        manzil = manzil,
                        iib_manzil = iib_manzil,
                        pasport = a.pasport_serya_raqam,
                        ttj_nomer=ttj_nomer
                    )
                    data.save()
                    print('yangi kiritildi')


        else:
            ariza = 'Hozirda ariza mavjud emas'

    for t in talaba_id:
        import qrcode
        import datetime as dt


        data = f"https://ttj.kspi.uz/ariza/shartnomalar/{t.id}/"  # QR-kodga kiritmoqchi bo'lgan ma'lumot

        # QR-kod obyektini yaratish
        qr = qrcode.QRCode(version=1, box_size=10, border=4)

        # Ma'lumotni QR-kodga qo'shish
        qr.add_data(data)

        # QR-kodni yaratish
        qr.make()

        # QR-koddan tasvir yaratish
        img = qr.make_image()

        # Tasvirni saqlash
        img.save(f"media/code/qrcode{t.id}.png")
        
        link = f'http://ttj.kspi.uz/media/code/qrcode{t.id}.png'
        rasmlar = Rasm.objects.filter(talaba_id=t.id)
        qrcode = Rasm.objects.filter(talaba_id=t.id)
        
        
        media_url = '/code/'
        image_path = f'qrcode{t.id}.png'
        image_url = f'{media_url}{image_path}'
        if rasmlar:
            data = get_object_or_404(Rasm, talaba_id=t.id)
            data.talaba_id = t.id
            data.link = link 
            data.rasm = image_url
            data.save()
            print('update qilindi')
        else:
            data = Rasm.objects.create(
                talaba_id = t.id,
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
        'ariza':ariza,
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
        imtiyoz_turi = 'Talabada imtiyoz mavjud emas!!!'  
    
    
    if request.method == 'POST': 
        ttj_nomer = request.POST['ttj_nomer']       
        qavat = request.POST['qavat']
        xona = request.POST['xona']        
        
        if order_id:
            for t in order_id:
                data = get_object_or_404(Order, talaba_id=pk)
                data.ttj_nomer = ttj_nomer
                data.qavat = qavat
                data.xona = xona 
                data.tasdiqlash='tasdiqlandi'               
                data.save()
                return redirect('/ariza/barcha_orderlar/')
        else:        
            data = Order.objects.create(
                kiritish = 'kiritildi',xona=xona,
                ttj_nomer=ttj_nomer, qavat=qavat,
                tasdiqlash='tasdiqlandi',                
            )
            data.save()
            return redirect('/ariza/barcha_orderlar/')
    
    contex = {
        'talabalar':talabalar,'arizalar':arizalar,'imtiyoz':imtiyoz,'rasm_url':rasm_url,
        'imtiyoz_url':imtiyoz_url,'familya':familya,'ism':ism,'sharif':sharif,'telefon':telefon,
        'pasport':pasport,'imtiyoz_turi':imtiyoz_turi,'fakultet':fakultet,'yonalish':yonalish,
        'kurs':kurs,'viloyat':viloyat,'tuman':tuman,'kocha':kocha,
    }
    return render(request, 'superadmin/order_berish.html', contex)


def barcha_orderlar(request):
    arizalar = Ariza.objects.filter(tasdiqlash='tasdiqlandi') 
    orderlar = Order.objects.filter(tasdiqlash='')   
    if arizalar:        
        for a in arizalar:
            manzil = f'{a.viloyat} {a.tuman}'
            if Order.objects.filter(talaba_id=a.talaba_id):
                data = get_object_or_404(Order, talaba_id=a.talaba_id)
                data.familiya=a.last_name
                data.ism=a.first_name
                data.sharif=a.sharif
                data.fakultet=a.fakultet
                data.yonalish=a.yonalish
                data.kurs=a.kurs
                data.manzil=manzil                
                print('update qilinyapti')            
            else:
                data = Order.objects.create(
                    talaba_id=a.talaba_id,familiya=a.last_name,ism=a.first_name,
                    sharif=a.sharif,fakultet=a.fakultet,yonalish=a.yonalish,
                    kurs=a.kurs,manzil=manzil
                )
                data.save()
                print('yangi qo`shildi') 
                
    else:
        arizalar = '' 
  
        
    
    contex = {
       'arizalar':arizalar,
       'orderlar':orderlar,       
    }
    return render(request, 'superadmin/barcha_orderlar.html', contex)



@csrf_exempt
def order_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=talabalar.csv'

    writer = csv.writer(response)
    
    
    writer.writerow([
        'Shartnoma raqami',
        'Talaba F.I.SH',                           
    ])   
    
    orderlar  = Order.objects.filter(tasdiqlash='tasdiqlandi')
    if orderlar:
        for o in orderlar:
            writer.writerow([
                o.id,
                o.familiya
            ])
    else:
        return redirect('/ariza/barcha_orderlar/')
    

    return response
