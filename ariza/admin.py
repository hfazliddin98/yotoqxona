from django.contrib import admin
from .models import Ariza, Tolov, Tark_etgan


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

