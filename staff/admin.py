from django.contrib import admin
from .models import *

@admin.register(Provincialstaff,Districtstaff,Staff,Title,Position,Userlevel)
class ViewAdmin(admin.ModelAdmin):
	pass
