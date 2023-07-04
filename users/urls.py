from django.urls import path
from users.views import home, kirish, royhat, superadmin, dekanatadmin, talaba
from users.views import superadmin_qoshish, dekanatadmin_qoshish

urlpatterns = [
   path('', home, name='home'),
   path('kirish/', kirish, name='kirish'),
   path('royhat/', royhat, name='royhat'),
   path('superadmin/', superadmin, name='superadmin'),
   path('dekanatadmin/', dekanatadmin, name='dekanatadmin'), 
   path('talaba/', talaba, name='talaba'),  
   path('superadmin_qoshish/', superadmin_qoshish, name='superadmin_qoshish'),
   path('dekanatadmin_qoshish/', dekanatadmin_qoshish, name='dekanatadmin_qoshish'),
]
