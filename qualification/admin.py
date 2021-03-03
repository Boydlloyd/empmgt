from django.contrib import admin
from .models import *

@admin.register(Category,Categorylevel,Qualification,Maindocument,Staffdocument)
class ViewAdmin(admin.ModelAdmin):
    pass
