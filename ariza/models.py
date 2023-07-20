from django.db import models


class Ariza(models.Model):
    talaba_id = models.CharField(max_length=100)
    viloyat = models.CharField(max_length=100)
    tuman = models.CharField(max_length=100)
    kocha = models.CharField(max_length=100)
    fakultet = models.CharField(max_length=100)
    yonalish = models.CharField(max_length=100)
    kurs    = models.CharField(max_length=100)
    pasport_serya_raqam = models.CharField(max_length=100)    
    pasport_rasm = models.FileField(upload_to='rasmlar/')
    
    # imtiyozlarni kiritish
    imtiyoz_nomi = models.CharField(max_length=100)
    imtiyoz_file = models.FileField(upload_to='imtiyoz/')
    
    # xulosa kiritish
    xulosa = models.CharField(max_length=1000, blank=True)
    
    # tasqiqlash
    tasdiqlash = models.CharField(max_length=100, blank=True)       
    sana = models.DateTimeField(auto_now_add=True)
    
    
class Tolov(models.Model):
    talaba_id = models.CharField(max_length=100)
    narhi = models.CharField(max_length=100)
    kivtansiya = models.FileField(upload_to='kivtansiya/')
    tasdiqlash = models.CharField(max_length=100, blank=True)
    sana = models.DateTimeField(auto_now_add=True)
    
class Barcha_tolov(models.Model):
    barcha = models.CharField(max_length=100, blank=True)
    oylik = models.CharField(max_length=100, blank=True)
    boshlanginch_tolov = models.CharField(max_length=100, blank=True)
    hisob_raqam = models.CharField(max_length=100, blank=True)
    sana = models.DateTimeField(auto_now_add=True)
    
class Tark_etgan(models.Model):
    talaba_id  = models.CharField(max_length=100)
    tark_etish = models.CharField(max_length=100)
    sabab = models.CharField(max_length=300)
    sana = models.DateTimeField(auto_now_add=True)
    
    

    
    

