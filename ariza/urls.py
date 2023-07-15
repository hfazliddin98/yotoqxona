from django.urls import path
from .views import arizalar, imtiyozlar, barcha_arizalar, tasdiqlangan_ariza, radetilgan_ariza
from .views import tasdiqlangan, radetilgan, talaba_malumotlar, talaba_tolov, tolov_tasdiqlash, barcha_tolovlar


urlpatterns = [
   path('arizalar/', arizalar, name='arizalar'),
   path('imtiyozlar/', imtiyozlar, name='imtiyozlar'),
   path('barcha_arizalar/', barcha_arizalar, name='barcha_arizalar'),
   path('tasdiqlangan_ariza/<str:pk>/', tasdiqlangan_ariza, name='tasdiqlangan_ariza'),
   path('radetilgan_ariza/<str:pk>/', radetilgan_ariza, name='radetilgan_ariza'),
   path('radetilgan/', radetilgan, name='radetilgan'),
   path('tasdiqlangan/', tasdiqlangan, name='tasdiqlangan'),
   path('talaba_malumotlar/<str:pk>/', talaba_malumotlar, name='talaba_malumotlar'),
   path('talaba_tolov/', talaba_tolov, name='talaba_tolov'),
   path('tolov_tasdiqlash/<str:pk>/', tolov_tasdiqlash, name='tolov_tasdiqlash'),
   path('barcha_tolovlar/', barcha_tolovlar, name='barcha_tolovlar'),
]
