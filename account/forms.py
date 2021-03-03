from django import forms
from .models import Newuser,Serviceprovider,Mobileformat
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

class RoleForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(RoleForm, self).__init__(*args, **kwargs)
		self.fields['name'].required = True

	name=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Role Name"}))
	class Meta:
		model=Group
		fields=('name',)
  


class RegisterUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username',)
               
        
class RegisterNewuser(forms.ModelForm):
    userid=forms.CharField(label='Username',widget=forms.TextInput(attrs={"placeholder":"Username"}))
    fname=forms.CharField(label='First Name',widget=forms.TextInput(attrs={"placeholder":"First Name"}))
    lname=forms.CharField(label='Last Name',widget=forms.TextInput(attrs={"placeholder":"Last Name"}))
    mobile=forms.CharField(label='Contact No.',widget=forms.TextInput(attrs={"placeholder":"Contact No."}))
    email=forms.CharField(label='Email',widget=forms.TextInput(attrs={"placeholder":"Email"}))
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))

    class Meta:
        model=Newuser
        fields=('userid','fname','lname','email','mobile','password1','password2')   
        
        
        
class CreateNewuser(forms.ModelForm):
    userid=forms.CharField(label='Username',widget=forms.TextInput(attrs={"placeholder":"Username"}))
    fname=forms.CharField(label='First Name',widget=forms.TextInput(attrs={"placeholder":"First Name"}))
    lname=forms.CharField(label='Last Name',widget=forms.TextInput(attrs={"placeholder":"Last Name"}))
    email=forms.CharField(label='Email',widget=forms.TextInput(attrs={"placeholder":"Email"}))
    mobile=forms.CharField(label='Contact No.',widget=forms.TextInput(attrs={"placeholder":"Contact No."}))
    class Meta:
        model=Newuser
        fields=('userid','fname','lname','mobile','email')   
            

class ProviderForm(forms.ModelForm):
    provider=forms.CharField(label='Service Provider',widget=forms.TextInput(attrs={"placeholder":"Service Provider Name"}))
    class Meta:
        model=Serviceprovider
        fields=('provider',)   
               
        
class MobileformatForm(forms.ModelForm):
    mformat=forms.CharField(label='Format',widget=forms.TextInput(attrs={"placeholder":"Mobile Format"}))
    class Meta:
        model=Mobileformat
        fields=('mformat','length','provider')     
 


     
        

