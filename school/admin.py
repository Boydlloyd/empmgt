from django.contrib import admin
from .models import *

@admin.register(Province,District,School)
class ViewAdmin(admin.ModelAdmin):
	pass