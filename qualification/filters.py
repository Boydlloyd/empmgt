import django_filters
from django_filters import CharFilter
from .models import *
from django import forms

class QualificationFilter(django_filters.FilterSet):
	field=CharFilter(label='Field of Study',field_name='field',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"Search Field"}))
	class Meta:
		model=Qualification
		fields=('field','category','level')
  
class CategoryFilter(django_filters.FilterSet):
    category=CharFilter(label='Category of Study',field_name='category',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"Search Category"}))
    class Meta:
        model=Category
        fields=('category',)  
  
  
class CategorylevelFilter(django_filters.FilterSet):
    level=CharFilter(label='Level of Study',field_name='level',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"Search Level"}))
    class Meta:
        model=Category
        fields=('level',) 
        
        
class MaindocumentFilter(django_filters.FilterSet):
    docttype=CharFilter(label='',field_name='docttype',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"Document Type"}))
    class Meta:
        model=Maindocument
        fields=('docttype',)     
