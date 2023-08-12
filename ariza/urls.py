from django.urls import path
from .views import ariza, arizalar, ariza_imtiyoz, barcha_arizalar, tasdiqlangan_ariza, radetilgan_ariza, tark_etish
from .views import tasdiqlangan, radetilgan, talaba_tolov, tolov_tasdiqlash, tolov_radetish, barcha_tolovlar
from .views import hisob_varoq, tolov_chek, shartnoma, shartnomalar, order, tark_etgan_talaba, tolovlar, tasdiqlangan_tolov
from .views import superadminlar, dekanatadminlar
from .views import talaba_malumotlar, radetilgan_malumotlar, tasdiqlangan_malumotlar, tark_etgan_malumotlar
from .views import talaba_tolov_malumotlar, radetilgan_tolov_malumotlar
from .views import imtiyoz, imtiyozli_arizalar, imtiyoz_malumotlar, imtiyozni_tasdiqlash, imtiyozni_radetish, tasdiqlangan_imtiyoz_malumotlar
from .views import arizalar_jadvali, tasdiqlangan_imtiyozli_arizalar
from .views import dekanat_barcha_arizalar, dekanat_tasdiqlangan_arizalar, dekanat_radetilgan_arizalar
from .views import dekanat_barcha_malumot, dekanat_tasdiqlangan_malumot, dekanat_radetilgan_malumot
from .views import barcha_orderlar, order_berish, order_csv, tolov_csv
from .views import dekanat_tasdiqlangan_ariza, dekanat_radetilgan_ariza, ariza_csv


urlpatterns = [
   # arizalaruchun  
   path('barcha_arizalar/', barcha_arizalar, name='barcha_arizalar'),
   path('arizalar_jadvali/<str:pk>/', arizalar_jadvali, name='arizalar_jadvali'),
   
   
   path('tasdiqlangan_ariza/<str:pk>/', tasdiqlangan_ariza, name='tasdiqlangan_ariza'),
   path('radetilgan_ariza/<str:pk>/', radetilgan_ariza, name='radetilgan_ariza'),
   path('radetilgan/', radetilgan, name='radetilgan'),
   path('tasdiqlangan/', tasdiqlangan, name='tasdiqlangan'),
   
   # imtiyozlar uchun
   path('imtiyoz/', imtiyoz, name='imtiyoz'), 
   path('imtiyozli_arizalar/', imtiyozli_arizalar, name='imtiyozli_arizalar'),  
   path('tasdiqlangan_imtiyozli_arizalar/', tasdiqlangan_imtiyozli_arizalar, name='tasdiqlangan_imtiyozli_arizalar'), 
   path('imtiyoz_malumotlar/<str:pk>/', imtiyoz_malumotlar, name='imtiyoz_malumotlar'),
   path('imtiyozni_tasdiqlash/<str:pk>/', imtiyozni_tasdiqlash, name='imtiyozni_tasdiqlash'),
   path('imtiyozni_radetish/<str:pk>/', imtiyozni_radetish, name='imtiyozni_radetish'),
   path('tasdiqlangan_imtiyoz_malumotlar/<str:pk>/', tasdiqlangan_imtiyoz_malumotlar, name='tasdiqlangan_imtiyoz_malumotlar'),
   
   # talaba uchun
   path('ariza/', ariza, name='ariza'), 
   path('arizalar/', arizalar, name='arizalar'), 
   path('ariza_imtiyoz/', ariza_imtiyoz, name='ariza_imtiyoz'), 
   path('ariza_csv/', ariza_csv, name='ariza_csv'),
   
   # tolvlar uchun
   path('talaba_tolov/', talaba_tolov, name='talaba_tolov'),
   path('tasdiqlangan_tolov/', tasdiqlangan_tolov, name='tasdiqlangan_tolov'),
   path('tolov_tasdiqlash/<str:pk>/', tolov_tasdiqlash, name='tolov_tasdiqlash'),
   path('tolov_radetish/<str:pk>/', tolov_radetish, name='tolov_radetish'),
   path('barcha_tolovlar/', barcha_tolovlar, name='barcha_tolovlar'),
   path('tark_etish/', tark_etish, name='tark_etish'),
   path('tark_etgan_talaba/', tark_etgan_talaba, name='tark_etgan_talaba'),
   path('hisob_varoq/', hisob_varoq, name='hisob_varoq'),
   path('tolov_chek/', tolov_chek, name='tolov_chek'),
   path('tolovlar/<str:pk>/', tolovlar, name='tolovlar'),
   path('tolov_csv/', tolov_csv, name='tolov_csv'),

   # shartnomalar
   path('shartnoma/<str:pk>/', shartnoma, name='shartnoma'),   
   path('shartnomalar/', shartnomalar, name='shartnomalar'),
   
   # orderlar
   path('order/<str:pk>/', order, name='order'),
   path('order_berish/<str:pk>/', order_berish, name='order_berish'),
   path('barcha_orderlar/', barcha_orderlar, name='barcha_orderlar'),
   path('order_csv/', order_csv, name='order_csv'),
   
   # royhatlar
   path('superadminlar/', superadminlar, name='superadminlar'),   
   path('dekanatadminlar/', dekanatadminlar, name='dekanatadminlar'),
   
   # ariza malumot
   path('talaba_malumotlar/<str:pk>/', talaba_malumotlar, name='talaba_malumotlar'),
   path('tasdiqlangan_malumotlar/<str:pk>/', tasdiqlangan_malumotlar, name='tasdiqlangan_malumotlar'),
   path('radetilgan_malumotlar/<str:pk>/', radetilgan_malumotlar, name='radetilgan_malumotlar'),
   path('tark_etgan_malumotlar/<str:pk>/', tark_etgan_malumotlar, name='tark_etgan_malumotlar'),
    
   # tolov malumot
   path('talaba_tolov_malumotlar/<str:pk>/', talaba_tolov_malumotlar, name='talaba_tolov_malumotlar'),
   path('radetilgan_tolov_malumotlar/<str:pk>/', radetilgan_tolov_malumotlar, name='radetilgan_tolov_malumotlar'),
   
   # dekanat uchun
   path('dekanat_barcha_arizalar/', dekanat_barcha_arizalar, name='dekanat_barcha_arizalar'),
   path('dekanat_tasdiqlangan_arizalar/', dekanat_tasdiqlangan_arizalar, name='dekanat_tasdiqlangan_arizalar'),
   path('dekanat_radetilgan_arizalar/', dekanat_radetilgan_arizalar, name='dekanat_radetilgan_arizalar'),
   path('dekanat_barcha_malumot/<str:pk>/', dekanat_barcha_malumot, name='dekanat_barcha_malumot'),
   path('dekanat_tasdiqlangan_malumot/<str:pk>/', dekanat_tasdiqlangan_malumot, name='dekanat_tasdiqlangan_malumot'),
   path('dekanat_radetilgan_malumot/<str:pk>/', dekanat_radetilgan_malumot, name='dekanat_radetilgan_malumot'),
   path('dekanat_tasdiqlangan_ariza/<str:pk>/', dekanat_tasdiqlangan_ariza, name='dekanat_tasdiqlangan_ariza'),
   path('dekanat_radetilgan_ariza/<str:pk>/', dekanat_radetilgan_ariza, name='dekanat_radetilgan_ariza'),
]
