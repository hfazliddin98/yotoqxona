from django.db import models


class Ariza(models.Model):
    talaba_id = models.CharField(max_length=10)
    viloyat = models.CharField(max_length=100)
    tuman = models.CharField(max_length=100)
    fakultet = models.CharField(max_length=100)
    yonalish = models.CharField(max_length=100)
    kurs    = models.CharField(max_length=100)
    pasport_rasm = models.FileField(upload_to='rasmlar/')
    # imtiyozlarni kiritish
    nogironlig = models.CharField(max_length=100, blank=True)
    chin_yetim = models.CharField(max_length=100, blank=True)
    daftar_turishi = models.CharField(max_length=100, blank=True)
    boquvchisini_yoqotgan = models.CharField(max_length=100, blank=True)
    # tasqiqlash
    tasdiqlash = models.CharField(max_length=100, blank=True)
    radetish = models.CharField(max_length=100, blank=True)
    
    

