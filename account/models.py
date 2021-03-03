from django.db import models
from staff.models import Staff,Districtstaff,Provincialstaff,Userlevel
from django.contrib.auth.models import User,Permission


# Create your models here.

class UserHistory(models.Model):
	username = models.IntegerField()
	fname = models.CharField(max_length=25,blank=False)
	lname = models.CharField(max_length=25,blank=False)
	email = models.CharField(max_length=50,blank=True)
	role = models.CharField(max_length=10,blank=True)
	is_active = models.BooleanField(default=False)
	last_login= models.DateTimeField(max_length=30,null=True,blank=True)
	date_joined=models.DateTimeField(max_length=30,blank=False)
	datecreated= models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User,on_delete=models.DO_NOTHING)

	def __str__(self):
		return self.fname+" "+self.lname+": "+self.role

class Newuser(models.Model):
	userid = models.CharField(max_length=25,unique=True)
	fname = models.CharField(max_length=25)
	lname = models.CharField(max_length=25)
	mobile = models.CharField(max_length=20,null=True,unique=True)
	email = models.EmailField(max_length=50,unique=True)
	password1 = models.CharField(max_length=100)
	password2 = models.CharField(max_length=100)
	datecreated= models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.fname+" "+self.lname

class Serviceprovider(models.Model):
	provider = models.CharField(max_length=15,unique=True)
	datecreated= models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.provider


class Mobilelength(models.Model):
	length = models.IntegerField(default=10)
	datecreated= models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return str(self.length)

class Mobileformat(models.Model):
	mformat = models.CharField(max_length=10)
	provider = models.ForeignKey(Serviceprovider,on_delete=models.DO_NOTHING)
	length = models.ForeignKey(Mobilelength,on_delete=models.DO_NOTHING)
	datecreated= models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return str(self.mformat)+" "+self.provider.provider


class Usermodule(models.Model):
	datecreated= models.DateTimeField(auto_now_add=True)

class Useractivity(models.Model):
    datecreated= models.DateTimeField(auto_now_add=True)
 
class Setupmodule(models.Model):
	datecreated= models.DateTimeField(auto_now_add=True)