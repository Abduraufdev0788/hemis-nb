from django.contrib import admin
from .models import CustomUser, Parent

admin.site.register(CustomUser)
admin.site.register(Parent)