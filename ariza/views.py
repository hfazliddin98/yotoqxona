from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from ariza.models import Ariza, Tolov, Tark_etgan, Barcha_tolov, Shartnoma, Order, Rasm, Imtiyoz
from users.models import User


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

def arizalar(request):
    
    contex = {
        
    }
    return render(request, 'talaba/arizalar.html', contex)


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



def shartnomalar(request):
    
    contex = {
        
    }
    return render(request, 'talaba/shartnomalar.html', contex)

def tolovlar(request, pk):
    data = Tolov.objects.filter(talaba_id=pk)
    
    contex = {
        'data':data,
    }
    return render(request, 'talaba/tolovlar.html', contex)

#  superadmin arizalar

def barcha_arizalar(request):
    talaba = User.objects.filter(lavozim='talaba')
    arizalar = Ariza.objects.filter(tasdiqlash='')
   
    
   
    
    contex = {
        'talaba':talaba,
        'arizalar':arizalar,
    }
    return render(request, 'superadmin/barcha_arizalar.html', contex)


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

def imtiyozli_arizalar(request):
    talabalar = User.objects.filter(lavozim='talaba')
    imtiyozlar = Imtiyoz.objects.filter(tasdiqlash='')
    
    
    contex = {
        'talabalar':talabalar,
        'imtiyozlar':imtiyozlar,        
    }
    return render(request, 'superadmin/imtiyozli_arizalar.html', contex)


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
    return render(request, 'dekanatadmin/radetilgan_ariza.html', contex)

def tasdiqlangan(request):
    talabalar = User.objects.filter(lavozim='talaba')
    data = Ariza.objects.filter(tasdiqlash='tasdiqlandi')
    contex = {
        'data':data,
        'talabalar':talabalar,
    }
    return render(request,  'dekanatadmin/tasdiqlangan.html', contex)


def radetilgan(request):
    talabalar = User.objects.filter(lavozim='talaba')
    data = Ariza.objects.filter(tasdiqlash = 'radetildi')
    contex = {
        'data':data,
        'talabalar':talabalar,
    }
    return render(request,  'dekanatadmin/radetilgan.html', contex)


def talaba_malumotlar(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.all
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
    }
    return render(request, 'dekanatadmin/talaba_malumot.html', contex)

def tasdiqlangan_malumotlar(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.all
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
    }
    return render(request, 'dekanatadmin/tasdiqlangan_malumot.html', contex)

def radetilgan_malumotlar(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.all
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
    }
    return render(request, 'dekanatadmin/radetilgan_malumot.html', contex)


def tark_etgan_malumotlar(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.all
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
    }
    return render(request, 'dekanatadmin/tark_etgan_malumot.html', contex)

# talaba tolovlari haqida malumot dekanat uchun

def talaba_tolov_malumotlar(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.all
    tolov = Tolov.objects.all
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
        'tolov':tolov,
    }
    return render(request, 'dekanatadmin/talaba_tolov_malumot.html', contex)

def tasdiqlangan_tolov_malumotlar(request, pk):
    talabalar = User.objects.filter(id=pk)
    arizalar = Ariza.objects.all
    
    contex = {
        'talabalar':talabalar,
        'arizalar':arizalar,
    }
    return render(request, 'dekanatadmin/tasdiqlangan_tolov_malumot.html', contex)



def talaba_tolov(request):    
    if request.method == 'POST':
        talaba_id = request.user.id
        narhi = request.POST['narhi']
        kivtansiya = request.FILES['kivtansiya']
        
        if narhi == '':
            return redirect('/ariza/talaba_tolov/')
        else:        
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
    talaba = User.objects.filter(id=tolov.talaba_id)
    for t in talaba:
        ism  = t.first_name           
    data = get_object_or_404(Tolov, id=pk)                     
    data.tasdiqlash = 'tasdiqlandi'       
    data.save()
    
    contex = {
       'tolov':tolov, 
       'ism':ism,
    }
    return redirect('/ariza/barcha_tolovlar/', contex)


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
    return redirect('/ariza/barcha_tolovlar/', contex)

def tasdiqlangan_tolov(request, pk):
    talabalar = User.objects.get(id=pk)
    tolovlar = Tolov.objects.filter(tasdiqlash='tasdiqlandi')
    arizalar = Ariza.objects.all()  
    
    contex = {
        'tolovlar': tolovlar, 
        'talabalar':talabalar, 
        'arizalar':arizalar,      
    }
    return render(request, 'superadmin/tasdiqlangan_tolov.html', contex)


def superadminlar(request):
    
    contex = {
        
    }
    return render(request, 'superadmin/superadminlar.html', contex)

def dekanatadminlar(request):
    
    contex = {
        
    }
    return render(request, 'superadmin/dekanatadminlar.html', contex)

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
def tark_etgan_talaba(request):
    talabalar = User.objects.filter(lavozim='talaba')
    data = Tark_etgan.objects.filter(tark_etish='tark_etdi')
    
    contex = {
        'data':data,
        'talabalar':talabalar,
    }
    return render(request, 'superadmin/tark_etgan_talaba.html', contex)

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


def shartnoma(request):
    talaba_id = User.objects.all()
    for t in talaba_id:
        import qrcode

        data = f"https://shartnoma.kspi.uz/pdf/qrcode/{t.id}/"  # QR-kodga kiritmoqchi bo'lgan ma'lumot

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
        
        link = f'http://shartnoma.kspi.uz/media/code/qrcode{t.id}.png'
        rasmlar = Rasm.objects.filter(user_id=t.id)
        qrcode = Rasm.objects.filter(user_id=t.id)
        
        
        media_url = '/code/'
        image_path = f'qrcode{t.id}.png'
        image_url = f'{media_url}{image_path}'
        if rasmlar:
            data = get_object_or_404(Rasm, user_id=t.id)
            data.user_id = t.id
            data.link = link 
            data.rasm = image_url
            data.save()
            print('update qilindi')
        else:
            data = Rasm.objects.create(
                user_id = t.id,
                link = link,
                rasm = image_url
            )
            data.save()
            print('create qilindi')
    
    template_path = 'amaliyot/qrcode.html' 
    # sayt foydalanuvchisini va amaliyotni aniq ko`rsatish uchun ishlatiladi`   
    talaba_id = request.user.id   
    pdf = Shartnoma.objects.filter(talaba_id=pk)   
    
   
    
    hozir = dt.datetime.now()
    yil = hozir.year
    oy = hozir.month
    kun = hozir.day
    
    contex = {       
        'pdf':pdf,
        'yil':yil,
        'oy':oy,
        'kun':kun,
        'hozir':hozir,
        'qrcode':qrcode,              
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



