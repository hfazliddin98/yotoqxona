from django.contrib import admin
from .models import Ariza, Imtiyoz, Tolov


class ArizaAdmin(admin.ModelAdmin):
    list_display= [
        'id', 'talaba_id', 'viloyat', 'tuman'
    ]
admin.site.register(Ariza,ArizaAdmin)


class ImtiyozAdmin(admin.ModelAdmin):
    list_display= [
        'talaba_id','nomi'
    ]
admin.site.register(Imtiyoz, ImtiyozAdmin)

class TolovAdmin(admin.ModelAdmin):
    list_display= [
        'talaba_id','narhi', 'tasqiqlash'
    ]
admin.site.register(Tolov, TolovAdmin)

