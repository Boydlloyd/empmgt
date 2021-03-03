import django_filters
from django_filters import CharFilter
from .models import *
from django import forms

class StaffFilter(django_filters.FilterSet):
	search=CharFilter(label='Search Staff',field_name='search',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"School Staff"}))
	class Meta:
		model=Staff
		fields=('search','gender','position','isconfirmed','province','district','school','status')
  
class StaffFilter2(django_filters.FilterSet):
    search=CharFilter(label='Search Staff',field_name='search',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"School Staff"}))
    class Meta:
        model=Staff
        fields=('search','gender','position','isconfirmed','district','school','status')
  
class StaffFilter3(django_filters.FilterSet):
    search=CharFilter(label='Search Staff',field_name='search',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"School Staff"}))
    class Meta:
        model=Staff
        fields=('search','gender','position','isconfirmed','school','status')
  
class StaffFilter4(django_filters.FilterSet):
    search=CharFilter(label='Search Staff',field_name='search',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"School Staff"}))
    class Meta:
        model=Staff
        fields=('search','gender','position','isconfirmed','status')
  
class StaffFilterNone(django_filters.FilterSet):
    search=CharFilter(label='Search',field_name='search',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"","col":16,"row":0}))
    class Meta:
        model=Staff
        fields=('search',)

class DistrictStaffFilter(django_filters.FilterSet):
    search=CharFilter(label='Search Staff',field_name='search',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"District Staff"}))
    class Meta:
        model=Districtstaff
        fields=('search','gender','position','isconfirmed','province','district','status')
        
class DistrictStaffFilter2(django_filters.FilterSet):
    search=CharFilter(label='Search Staff',field_name='search',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"District Staff"}))
    class Meta:
        model=Districtstaff
        fields=('search','gender','position','isconfirmed','province','district','status')
        
class DistrictStaffFilter3(django_filters.FilterSet):
    search=CharFilter(label='Search Staff',field_name='search',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"District Staff"}))
    class Meta:
        model=Districtstaff
        fields=('search','gender','position','isconfirmed','status')
        

class DistrictStaffFilterNone(django_filters.FilterSet):
    search=CharFilter(label='Search Staff',field_name='search',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"District Staff"}))
    class Meta:
        model=Districtstaff
        fields=('search',)
  
class ProvincialStaffFilter(django_filters.FilterSet):
    search=CharFilter(label='Search Staff',field_name='search',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"Provincial Staff"}))
    class Meta:
        model=Provincialstaff
        fields=('search','gender','position','isconfirmed','province','status')
        
        
class ProvincialStaffFilter2(django_filters.FilterSet):
    search=CharFilter(label='Search Staff',field_name='search',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"Provincial Staff"}))
    class Meta:
        model=Provincialstaff
        fields=('search','gender','position','isconfirmed','status')
        
        
class ProvincialStaffFilter3(django_filters.FilterSet):
    search=CharFilter(label='Search Staff',field_name='search',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"Provincial Staff"}))
    class Meta:
        model=Provincialstaff
        fields=('search','gender','position','isconfirmed','status')
        
        
class ProvincialStaffFilter4(django_filters.FilterSet):
    search=CharFilter(label='Search Staff',field_name='search',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"Provincial Staff"}))
    class Meta:
        model=Provincialstaff
        fields=('search','gender','position','isconfirmed','status')
        
        
class ProvincialStaffFilterNone(django_filters.FilterSet):
    search=CharFilter(label='Search Staff',field_name='search',lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"Provincial Staff"}))
    class Meta:
        model=Provincialstaff
        fields=('search',)