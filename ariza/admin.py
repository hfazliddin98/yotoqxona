from django.contrib import admin
from .models import Ariza

# class ArizaAdmin(admin.ModelAdmin):
#     list_display= [
#         'id','viloyat','tuman','fakultet','yonalish','kurs','nogironlig','chin_yetim','daftar_turishi','boquvchisini_yoqotgan'
#     ]
# admin.site.register(Ariza,ArizaAdmin)

class ArizaAdmin(admin.ModelAdmin):
    list_display= [
        'id','viloyat','tuman'
    ]
admin.site.register(Ariza,ArizaAdmin)