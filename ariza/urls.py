from django.urls import path
from .views import arizalar


urlpatterns = [
   path('arizalar/', arizalar, name='arizalar'),
]
