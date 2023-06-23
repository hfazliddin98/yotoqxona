from django.db import models


class Ariza(models.Model):
    viloyat = models.CharField(max_length=100)
    tuman = models.CharField(max_length=100)
    fakultet = models.CharField(max_length=100)
    yonalish = models.CharField(max_length=100)
    kurs    = models.CharField(max_length=100)
    pasport_rasm = models.FileField(upload_to='pasport_rasm')
    # imtiyozlarni kiritish
    nogironlig = models.CharField(max_length=100)
    chin_yetim = models.CharField(max_length=100)
    daftar_turishi = models.CharField(max_length=100)
    boquvchisini_yoqotgan = models.CharField(max_length=100)
    
    