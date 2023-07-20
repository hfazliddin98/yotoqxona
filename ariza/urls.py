from django.urls import path
from .views import arizalar, barcha_arizalar, tasdiqlangan_ariza, radetilgan_ariza, tark_etish
from .views import tasdiqlangan, radetilgan, talaba_malumotlar, talaba_tolov, tolov_tasdiqlash, tolov_radetish, barcha_tolovlar
from .views import hisob_varoq, tolov_chek, shartnoma, order


urlpatterns = [
   path('arizalar/', arizalar, name='arizalar'),   
   path('barcha_arizalar/', barcha_arizalar, name='barcha_arizalar'),
   path('tasdiqlangan_ariza/<str:pk>/', tasdiqlangan_ariza, name='tasdiqlangan_ariza'),
   path('radetilgan_ariza/<str:pk>/', radetilgan_ariza, name='radetilgan_ariza'),
   path('radetilgan/', radetilgan, name='radetilgan'),
   path('tasdiqlangan/', tasdiqlangan, name='tasdiqlangan'),
   path('talaba_malumotlar/<str:pk>/', talaba_malumotlar, name='talaba_malumotlar'),
   path('talaba_tolov/', talaba_tolov, name='talaba_tolov'),
   path('tolov_tasdiqlash/<str:pk>/', tolov_tasdiqlash, name='tolov_tasdiqlash'),
   path('tolov_radetish/<str:pk>/', tolov_radetish, name='tolov_radetish'),
   path('barcha_tolovlar/', barcha_tolovlar, name='barcha_tolovlar'),
   path('tark_etish/', tark_etish, name='tark_etish'),
   path('hisob_varoq/', hisob_varoq, name='hisob_varoq'),
   path('tolov_chek/', tolov_chek, name='tolov_chek'),
   path('shartnoma/', shartnoma, name='shartnoma'),
   path('order/', order, name='order'),
]
