from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from ariza.models import Ariza, Tolov, Tark_etgan, Barcha_tolov, Shartnoma, Order, Rasm, Imtiyoz
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
    
    contex = {
        
    }
    return render(request, 'talaba/arizalar.html', contex)


@csrf_exempt
def ariza_imtiyoz(request):
    talaba_id = request.user.id
    talaba = User.objects.filter(id=talaba_id)
    ariza = Ariza.objects.filter(talaba_id=talaba_id)
    imtiyoz = Imtiyoz.objects.filter(talaba_id=talaba_id)
    
    contex = {
        'talaba':talaba,
        'ariza':ariza,
        'imtiyoz':imtiyoz,
    }
    return render(request, 'talaba/ariza_imtiyoz.html', contex)



# imtiyozlar bolimi uchun 
@csrf_exempt
def imtiyoz(request):
    talaba_id = request.user.id
    data = ''
    if request.method == 'POST':       
        imtiyoz_nomi = request.POST['imtiyoz_nomi']
        imtiyoz_file = request.FILES['imtiyoz_file']   
        
        if Imtiyoz.objects.filter(talaba_id=talaba_id):
            data = 'Bu foydalanuvchi imtiyoz yuborgan'
        else:
            data = Imtiyoz.objects.create(
                talaba_id=talaba_id, imtiyoz_nomi=imtiyoz_nomi, 
                imtiyoz_file=imtiyoz_file,               
            ) 
            data.save()          
            return redirect('/')   
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
    arizalar = Ariza.objects.filter(tasdiqlash='')   
    
    contex = {
        'talaba':talaba,
        'arizalar':arizalar,
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
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
        'imtiyoz':imtiyoz,
    }
    return render(request, 'superadmin/arizalar_jadvali.html', contex)


# imtiyoz uchun
@csrf_exempt
def imtiyozli_arizalar(request):
    talabalar = User.objects.filter(lavozim='talaba')
    imtiyozlar = Imtiyoz.objects.filter(tasdiqlash='')
    
    
    contex = {
        'talabalar':talabalar,
        'imtiyozlar':imtiyozlar,        
    }
    return render(request, 'superadmin/imtiyozli_arizalar.html', contex)

@csrf_exempt
def imtiyoz_malumotlar(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.all
    imtiyoz = Imtiyoz.objects.filter(talaba_id=pk)
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
        'imtiyoz':imtiyoz,
    }
    return render(request, 'superadmin/imtiyoz_malumotlar.html', contex)


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
    imtiyozlar = Imtiyoz.objects.filter(talaba_id=pk)
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
        'imtiyozlar':imtiyozlar,
    }
    return render(request, 'dekanatadmin/tasdiqlangan_malumot.html', contex)


@csrf_exempt
def radetilgan_malumotlar(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.filter(talaba_id=pk)
    imtiyozlar = Imtiyoz.objects.filter(talaba_id=pk)
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
        'imtiyozlar':imtiyozlar,
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
    if request.method == 'POST':
        barcha = request.POST['barcha']
        oylik = request.POST['oylik']
        boshlanginch_tolov = request.POST['boshlanginch_tolov']
        hisob_raqam = request.POST['hisob_raqam']
        
        data = Barcha_tolov.objects.create(
            barcha=barcha, oylik=oylik,
            boshlanginch_tolov=boshlanginch_tolov,
            hisob_raqam=hisob_raqam,
        )
        data.save()
        return redirect('/')
    
    contex = {
        
    }
    return render(request, 'superadmin/hisob_varoq.html', contex)


@csrf_exempt
def tolov_chek(request):
    
    
    contex = {
        
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
    
    contex = {        
        'yil':yil,
        'ariza':ariza,
        'oy':oy,
        'kun':kun,
        'hozir':hozir,
        'qrcode':qrcode,   
        'talaba':talaba,           
    }  
    return render(request, 'talaba/shartnomalar.html', contex)


@csrf_exempt
def shartnoma(request):
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
    shartnoma = Shartnoma.objects.filter(talaba_id=request.user.id)
    qrcode_rasm = Rasm.objects.filter(talaba_id=request.user.id)

    
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
def order(request):
    
    
    contex = {
        
    }
    
    template_path = 'talaba/order.html' 
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



