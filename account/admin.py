from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Newuser,UserHistory,Mobileformat,Serviceprovider,Mobilelength)
class ViewAdmin(admin.ModelAdmin):
    pass

