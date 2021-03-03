from django import forms
from .models import *

class QualificationForm(forms.ModelForm):
    field=forms.CharField(label='Field of Study',widget=forms.TextInput(attrs={"placeholder":"Field of Study"}))
    institute=forms.CharField(label='Name of Institution',widget=forms.TextInput(attrs={"placeholder":"Name of College/University"}))
    class Meta:
        model=Qualification
        fields=('category','level','field','institute','date_started','date_completed',)
        
        

class CategoryForm(forms.ModelForm):
    category=forms.CharField(label='Category',widget=forms.TextInput(attrs={"placeholder":"Category of Study"}))
    class Meta:
        model=Category
        fields=('category',)
        
class MaindocumentForm(forms.ModelForm):
    docttype=forms.CharField(label='Document Type',widget=forms.TextInput(attrs={"placeholder":"Document Type"}))
    description=forms.CharField(label='Description',widget=forms.Textarea(attrs={"placeholder":"Description"}))
    class Meta:
        model=Maindocument
        fields=('docttype','description','is_active',)  


class UploadMainDocumentForm(forms.ModelForm):
    class Meta:
        model=Staffdocument
        fields=('documentupload',) 
        
        
class CategoryLevelForm(forms.ModelForm):
    level=forms.CharField(label='Level',widget=forms.TextInput(attrs={"placeholder":"Level of Study"}))
    class Meta:
        model=Categorylevel
        fields=('level',)
        
        
        
class UploadDocumentForm(forms.ModelForm):
    doctitle=forms.CharField(label='Document Title',widget=forms.TextInput(attrs={"placeholder":"Title of Document"}))
    class Meta:
        model=Documentupload
        fields=('documentupload','doctitle') 