from django.urls import path
from users.views import home, kirish, royhat, superadmin, dekanatadmin, talaba

urlpatterns = [
   path('', home, name='home'),
   path('kirish/', kirish, name='kirish'),
   path('royhat/', royhat, name='royhat'),
   path('superadmin/', superadmin, name='superadmin'),
   path('dekanatadmin/', dekanatadmin, name='dekanatadmin'), 
   path('talaba/', talaba, name='talaba'),  
]
