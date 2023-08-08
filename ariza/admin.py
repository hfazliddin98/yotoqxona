from django.contrib import admin
from .models import Ariza, Tolov, Tark_etgan, Barcha_tolov, Imtiyoz, Shartnoma, Rasm, Order, Order_link


class ArizaAdmin(admin.ModelAdmin):
    list_display= [
        'id', 'talaba_id', 'viloyat', 'tuman','sana'
    ]
    search_fields = ['id', 'talaba_id']
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


class ShartnomaAdmin(admin.ModelAdmin):
    list_display= [
        'id'
    ]
admin.site.register(Shartnoma, ShartnomaAdmin)


class RasmAdmin(admin.ModelAdmin):
    list_display= [
        'id'
    ]
admin.site.register(Rasm, RasmAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display= [
        'id'
    ]
admin.site.register(Order, OrderAdmin)


class Order_linkAdmin(admin.ModelAdmin):
    list_display= [
        'id'
    ]
admin.site.register(Order_link, Order_linkAdmin)

