from django import forms
from .models import*

class ProvinceForm(forms.ModelForm):
	province=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Province Name"}))
	class Meta:
		model=Province
		fields=('province',)

class DistrictForm(forms.ModelForm):
	district=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"District Name"}))
	class Meta:
		model=District
		fields=('district',)

class SchoolForm(forms.ModelForm):
	school_code=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"School Code"}))
	school_name=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"School Name"}))
	school_address=forms.CharField(widget=forms.Textarea(attrs={"placeholder":"School Address"}))
	class Meta:
		model=School
		fields=('district','school_code','school_name','school_address')

class UpdateSchoolForm(forms.ModelForm):
	school_code=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"School Code"}))
	school_name=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"School Name"}))
	school_address=forms.CharField(widget=forms.Textarea(attrs={"placeholder":"School Address"}))
	class Meta:
		model=School
		fields=('school_code','school_name','school_address','district',)
  
  
  
class ExportSchool(forms.ModelForm):
    class Meta:
        model=School
        fields=('export_to_file',)
        labels={'export_to_file':'',}