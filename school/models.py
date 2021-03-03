from django.db import models
from django.contrib.auth.models import User
import datetime

class Schoolmodule(models.Model):
    datecreated= models.DateTimeField(auto_now_add=True)

def current_date_time():
	current = datetime.datetime.now()
	newcurrent = str(current)
	mydate=newcurrent[0:19]
	return mydate

class Province(models.Model):
    province = models.CharField("Province",max_length=30,unique=True)
    datecreated= models.DateTimeField(auto_now_add=True)
    districtnumber = models.IntegerField(default=0)
    schoolnumber = models.IntegerField(default=0)
    staffnumber = models.IntegerField(default=0)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.province

class District(models.Model):
    district = models.CharField("Location",max_length=30,unique=True)
    datecreated= models.DateTimeField(auto_now_add=True)
    province = models.ForeignKey(Province,on_delete=models.DO_NOTHING)
    schoolnumber = models.IntegerField(default=0)
    staffnumber = models.IntegerField(default=0)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.district

class School(models.Model):
    school_code = models.IntegerField(unique=True)
    school_name = models.CharField("School Name",max_length=50,unique=True)
    school_address = models.CharField("Address",max_length=50,unique=True)
    staffnumber = models.IntegerField(default=0)
    district = models.ForeignKey(District,on_delete=models.DO_NOTHING)
    province = models.ForeignKey(Province,on_delete=models.DO_NOTHING)
    datecreated= models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.school_name