from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User


class Useradmin(admin.ModelAdmin):
    list_display = [
        'id', 'username', 'first_name', 'last_name', 'parol'
    ]
    search_fields = ['username', 'id']
    
admin.site.register(User, Useradmin)
admin.site.unregister(Group)
