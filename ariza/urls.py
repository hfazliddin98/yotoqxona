from django.urls import path
from .views import ariza_get, ariza_post, ariza_update, ariza_delete

urlpatterns = [
    path('get/', ariza_get),
    path('post/', ariza_post),
    path('update/<int:id>/', ariza_update),
    path('delete/<int:id>/', ariza_delete)
]
