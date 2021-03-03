import django_filters
from django_filters import CharFilter
from .models import *
from django import forms

class SchoolFilter(django_filters.FilterSet):
	school_name=CharFilter(label='Search School',field_name='school_name',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"School Name"}))
	class Meta:
		model=School
		fields=('school_name','province','district',)


class SchoolFilter2(django_filters.FilterSet):
	school_name=CharFilter(label='Search School',field_name='school_name',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"School Name"}))
	class Meta:
		model=School
		fields=('school_name','district',)


class SchoolFilter3(django_filters.FilterSet):
	school_name=CharFilter(label='Search School',field_name='school_name',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"School Name"}))
	class Meta:
		model=School
		fields=('school_name',)
  
  
class SchoolFilterNone(django_filters.FilterSet):
	school_name=CharFilter(label='Search School',field_name='school_name',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"School Name"}))
	class Meta:
		model=School
		fields=('school_name',)

class DistrictFilter(django_filters.FilterSet):
	district=CharFilter(label='Search District',field_name='district',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"District Name"}))
	class Meta:
		model=District
		fields=('district','province',)


