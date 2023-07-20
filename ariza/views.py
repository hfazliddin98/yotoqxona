from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from ariza.models import Ariza, Tolov, Tark_etgan, Barcha_tolov
from users.models import User


def arizalar(request):
    talaba_id = request.user.id
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
        imtiyoz_nomi = request.POST['imtiyoz_nomi']
        imtiyoz_file = request.FILES['imtiyoz_file']   
        serya = f'{pasport_serya} {pasport_raqam}'
        print(serya)     
        
        if Ariza.objects.filter(pasport_serya_raqam=serya):
            data = 'Bu foydalanuvchi ariza yuborgan'
        else:
            ariza = Ariza.objects.create(
                talaba_id=talaba_id, viloyat = viloyat, tuman = tuman,
                kocha=kocha, fakultet = fakultet, yonalish=yonalish,
                kurs = kurs, pasport_serya_raqam=serya,
                pasport_rasm=pasport_rasm, imtiyoz_nomi=imtiyoz_nomi, 
                imtiyoz_file=imtiyoz_file,               
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
    
    
    contex = {
        
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



