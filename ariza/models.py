from django.db import models


class Ariza(models.Model):
    talaba_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    sharif = models.CharField(max_length=100)
    viloyat = models.CharField(max_length=100)
    tuman = models.CharField(max_length=100)
    kocha = models.CharField(max_length=100)
    fakultet = models.CharField(max_length=100)
    yonalish = models.CharField(max_length=100)
    kurs    = models.CharField(max_length=100)
    pasport_serya_raqam = models.CharField(max_length=100)    
    pasport_rasm = models.FileField(upload_to='rasmlar/')    
   
    # xulosa kiritish
    xulosa = models.CharField(max_length=1000, blank=True)
    
    # tasqiqlash
    tasdiqlash = models.CharField(max_length=100, blank=True)       
    sana = models.DateTimeField(auto_now_add=True)


class Imtiyoz(models.Model):
    talaba_id = models.CharField(max_length=100)
    imtiyoz_nomi = models.CharField(max_length=100)
    imtiyoz_file = models.FileField(upload_to='imtiyoz/')
    tasdiqlash = models.CharField(max_length=100, blank=True)
    # xulosa kiritish
    xulosa = models.CharField(max_length=1000, blank=True)
    sana = models.DateField(auto_now_add=True)
    
class Tolov(models.Model):
    talaba_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    sharif = models.CharField(max_length=100)
    narhi = models.CharField(max_length=100)
    kivtansiya = models.FileField(upload_to='kivtansiya/')
    tasdiqlash = models.CharField(max_length=100, blank=True)
    sana = models.DateTimeField(auto_now_add=True)
    
class Barcha_tolov(models.Model):
    yillik_tolv = models.CharField(max_length=100)
    oylik = models.CharField(max_length=100, blank=True)
    boshlanginch_tolov = models.CharField(max_length=100, blank=True)
    yigilgan_summa = models.CharField(max_length=100, blank=True)
    ttj_soni = models.CharField(max_length=100, blank=True)
    xonalar_soni = models.CharField(max_length=100, blank=True)    
    sana = models.DateTimeField(auto_now_add=True)
    
class Tark_etgan(models.Model):
    talaba_id  = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    sharif = models.CharField(max_length=100)
    tark_etish = models.CharField(max_length=100)
    sabab = models.CharField(max_length=300)
    sana = models.DateTimeField(auto_now_add=True)
    
    
class Shartnoma(models.Model):
    talaba_id = models.CharField(max_length=100)    
    talaba_f_i_sh = models.CharField(max_length=100, blank=True)
    manzil = models.CharField(max_length=100, blank=True)    
    iib_manzil = models.CharField(max_length=200, blank=True)   
    pasport = models.CharField(max_length=100, blank=True)    
    ttj_nomer = models.CharField(max_length=100, blank=True)
   
   
class Rasm(models.Model):
    talaba_id = models.CharField(max_length=100)    
    link = models.CharField(max_length=100, blank=True)
    rasm = models.FileField(upload_to='qrcode/')  
    
class Order_link(models.Model):
    talaba_id = models.CharField(max_length=100)    
    link = models.CharField(max_length=100, blank=True)
    rasm = models.FileField(upload_to='order_qrcode/')  
    
    
class Order(models.Model):
    talaba_id = models.CharField(max_length=100)    
    familiya = models.CharField(max_length=100, blank=True)
    ism = models.CharField(max_length=100, blank=True)    
    sharif = models.CharField(max_length=200, blank=True)   
    manzil = models.CharField(max_length=100, blank=True)    
    fakultet = models.CharField(max_length=100, blank=True)
    yonalish = models.CharField(max_length=10, blank=True)    
    kurs = models.CharField(max_length=100, blank=True)
    guruh = models.CharField(max_length=100, blank=True)       
    ttj_nomer = models.CharField(max_length=100, blank=True)
    qavat = models.CharField(max_length=10, blank=True)    
    xona = models.CharField(max_length=100, blank=True)
    sana = models.DateTimeField(auto_now_add=True)

    
    

