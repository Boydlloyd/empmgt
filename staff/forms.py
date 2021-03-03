from django import forms
from .models import*
from account.models import Newuser

class PositionForm(forms.ModelForm):
	position=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Position Name"}))
	class Meta:
		model=Position
		fields=('position',)


class TitleForm(forms.ModelForm):
	title=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Title Name"}))
	class Meta:
		model=Title
		fields=('title',)

class UpdateStaffForm(forms.ModelForm):
    empnumber=forms.CharField(label="Employee No.", widget=forms.TextInput(attrs={"placeholder":"Title Name"}))
    tsnumber=forms.CharField(label="TS No.",widget=forms.TextInput(attrs={"placeholder":"TS No."}))
    fname=forms.CharField(label="First Name",widget=forms.TextInput(attrs={"placeholder":"First Name"}))
    lname=forms.CharField(label="Last Name",widget=forms.TextInput(attrs={"placeholder":"Last Name"}))
    mname=forms.CharField(label="Middle Name",widget=forms.TextInput(attrs={"placeholder":"Middle Name"}))
    nrc=forms.CharField(label="NRC Number",widget=forms.TextInput(attrs={"placeholder":"NRC Number"}))
    class Meta:
        model=Staff
        fields=('empnumber','tsnumber','fname','lname','mname','nrc','gender','title','birth_date','first_appointment','isconfirmed','position','school')

class UpdateStaffBioForm(forms.ModelForm):
    fname=forms.CharField(label="First Name",widget=forms.TextInput(attrs={"placeholder":"First Name"}))
    lname=forms.CharField(label="Last Name",widget=forms.TextInput(attrs={"placeholder":"Last Name"}))
    mobile=forms.CharField(label="Contact No.",widget=forms.TextInput(attrs={"placeholder":"Contact No."}))
    class Meta:
        model=Staff
        fields=('title','fname','lname','mname','mobile','gender','district','birth_date')       
        
 
class UpdateStaffWorkForm(forms.ModelForm):
    nrc=forms.CharField(label="NRC Number",widget=forms.TextInput(attrs={"placeholder":"NRC Number"}))
    empnumber=forms.CharField(label="Employee No.", widget=forms.TextInput(attrs={"placeholder":"Epmloyee No."}))
    tsnumber=forms.CharField(label="TS No.",widget=forms.TextInput(attrs={"placeholder":"TS No."}))
    class Meta:
        model=Staff
        fields=('nrc','empnumber','tsnumber','first_appointment','isconfirmed','position',)      
       
        
class RegisterStaff(forms.ModelForm):
    userid=forms.CharField(label='Username',widget=forms.TextInput(attrs={"placeholder":"Username"}))
    fname=forms.CharField(label='First Name',widget=forms.TextInput(attrs={"placeholder":"First Name"}))
    lname=forms.CharField(label='Last Name',widget=forms.TextInput(attrs={"placeholder":"Last Name"}))
    email=forms.CharField(label='Email',widget=forms.TextInput(attrs={"placeholder":"Email"}))
    mobile=forms.CharField(label="Contact No.",widget=forms.TextInput(attrs={"placeholder":"Contact No."}))

    class Meta:
        model=Newuser
        fields=('userid','fname','lname','email','mobile')  
        
class DisapprovalForm(forms.ModelForm):
    comment=forms.CharField(label="Reason",widget=forms.Textarea(attrs={"placeholder":"Reason for Disapproval"}))
    class Meta:
        model=Staff
        fields=('comment',)       
        
class UploadStaffPhoto(forms.ModelForm):
    class Meta:
        model=Staff
        fields=('profilepic',)
        
        
class UploadDistrictStaffPhoto(forms.ModelForm):
    class Meta:
        model=Districtstaff
        fields=('profilepic',)
        

class UploadProvincialStaffPhoto(forms.ModelForm):
    class Meta:
        model=Provincialstaff
        fields=('profilepic',)
        
    
class UpdateDistrictStaffForm(forms.ModelForm):
    empnumber=forms.CharField(label="Employee No.",widget=forms.TextInput(attrs={"placeholder":"Employee No."}))
    fname=forms.CharField(label="First Name",widget=forms.TextInput(attrs={"placeholder":"First Name"}))
    lname=forms.CharField(label="Last Name",widget=forms.TextInput(attrs={"placeholder":"Last Name"}))
    nrc=forms.CharField(label="NRC.",widget=forms.TextInput(attrs={"placeholder":"NRC"}))
    mobile=forms.CharField(label="Contact No.",widget=forms.TextInput(attrs={"placeholder":"Contact No."}))
    class Meta:
        model=Districtstaff
        fields=('empnumber','title','fname','lname','nrc','mobile','gender','position','district')
        
        
class UpdateProvincialStaffForm(forms.ModelForm):
    empnumber=forms.CharField(label="Employee No.",widget=forms.TextInput(attrs={"placeholder":"Employee No."}))
    fname=forms.CharField(label="First Name",widget=forms.TextInput(attrs={"placeholder":"First Name"}))
    lname=forms.CharField(label="Last Name",widget=forms.TextInput(attrs={"placeholder":"Last Name"}))
    nrc=forms.CharField(label="NRC.",widget=forms.TextInput(attrs={"placeholder":"NRC"}))
    mobile=forms.CharField(label="Contact No.",widget=forms.TextInput(attrs={"placeholder":"Contact No."}))
    class Meta:
        model=Provincialstaff
        fields=('empnumber','title','fname','lname','nrc','mobile','gender','position','province')
        
        
        
class ExportStaff(forms.ModelForm):
    class Meta:
        model=Staff
        fields=('export_to_file',)
        labels={'export_to_file':'',}