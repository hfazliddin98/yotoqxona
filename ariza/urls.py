from django.urls import path
from .views import arizalar, imtiyozlar


urlpatterns = [
   path('arizalar/', arizalar, name='arizalar'),
   path('imtiyozlar/', imtiyozlar, name='imtiyozlar'),
]
