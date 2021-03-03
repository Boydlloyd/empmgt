import django_filters
from django_filters import CharFilter
from .models import *
from django import forms

class PermissionFilter(django_filters.FilterSet):
	codename=CharFilter(label='Search',field_name='codename',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"Permission"}))
	class Meta:
		model=Permission
		fields=('content_type','codename',)


class UserFilter(django_filters.FilterSet):
	username=CharFilter(label='Username',field_name='username',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"Username"}))
	class Meta:
		model=User
		fields=('username','is_active',)


