from django.contrib import admin
from .models import Ariza, Tolov, Tark_etgan, Barcha_tolov, Imtiyoz


class ArizaAdmin(admin.ModelAdmin):
    list_display= [
        'id', 'talaba_id', 'viloyat', 'tuman','sana'
    ]
admin.site.register(Ariza,ArizaAdmin)


class TolovAdmin(admin.ModelAdmin):
    list_display= [
        'id','talaba_id','narhi', 'tasdiqlash'
    ]
admin.site.register(Tolov, TolovAdmin)

class Tark_etganAdmin(admin.ModelAdmin):
    list_display= [
        'id', 'talaba_id', 'tark_etish'
    ]
admin.site.register(Tark_etgan, Tark_etganAdmin)


class Barcha_tolovAdmin(admin.ModelAdmin):
    list_display= [
        'id'
    ]
admin.site.register(Barcha_tolov, Barcha_tolovAdmin)

class ImtiyozAdmin(admin.ModelAdmin):
    list_display= [
        'id'
    ]
admin.site.register(Imtiyoz, ImtiyozAdmin)

