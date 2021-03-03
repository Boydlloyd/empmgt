from django.db import models
from django.contrib.auth.models import User,Group
from school.models import District,Province,School
import datetime

class Staffmodule(models.Model):
    datecreated= models.DateTimeField(auto_now_add=True)
    
class Myprofile(models.Model):
    datecreated= models.DateTimeField(auto_now_add=True)  
    
def current_date_time():
	current = datetime.datetime.now()
	newcurrent = str(current)
	mydate=newcurrent[0:19]
	return mydate

class Userlevel(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    userpic=models.ImageField("User Photo",upload_to='profile',default="profile/profile.jpg")
    staff = models.IntegerField(default=0)
    level= models.IntegerField()
    description = models.CharField("Description",null=True,max_length=30)
    def __str__(self):
        return str(self.user)+"_Level "+str(self.level)

    
class Position(models.Model):
    position = models.CharField("Staff Position",max_length=30,unique=True)
    datecreated= models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.position


class Title(models.Model):
    title = models.CharField("Staff Title",max_length=30,unique=True)
    datecreated= models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.title

class Staff(models.Model):
    GENDER = (('M', 'Male'),('F', 'Female'))
    STATUS = (('Registered', 'Registered'),('Pending', 'Pending'),('Updated', 'Updated'),('Approved', 'Approved'),('Disapproved', 'Disapproved'))
    tsnumber = models.CharField("TS Number",unique=True,null=True,max_length=8)
    fname = models.CharField("First Name",max_length=20)
    lname = models.CharField("Last Name",max_length=20)
    mname = models.CharField("Middle Name",max_length=20,blank=True)
    email = models.EmailField("Email",null=True,unique=True)
    gender = models.CharField("Gender",choices=GENDER,max_length=1)
    status = models.CharField("STATUS",choices=STATUS,max_length=11,default="Registered")
    isconfirmed = models.BooleanField(default=False)
    empnumber = models.CharField("Employee No.",unique=True,null=True,max_length=8)
    mobile=models.CharField("Contact No.", max_length=20,blank=True,null=True,unique=True)
    nrc = models.CharField("NRC",max_length=11,null=True)
    birth_date = models.DateField("Date of Birth", auto_now=False, null=True)
    first_appointment = models.DateField("Date of First Appointment", auto_now=False, null=True)
    title = models.ForeignKey(Title,null=True,on_delete=models.SET_NULL)
    position = models.ForeignKey(Position,null=True,on_delete=models.SET_NULL)
    school = models.ForeignKey(School,null=True,on_delete=models.SET_NULL)
    district = models.ForeignKey(District,null=True,on_delete=models.SET_NULL)
    province = models.ForeignKey(Province,null=True,on_delete=models.SET_NULL)
    datecreated= models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    search = models.CharField("Search",max_length=200,null=True)
    comment = models.CharField("Comment",max_length=200,default=" ")
    export_to_file=models.BooleanField(default=False)
    qualifications = models.IntegerField(default=0)
    profilepic=models.ImageField("Staff Photo",upload_to='profile',default="profile/profile.jpg")
    is_updated=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return self.fname +" "+self.lname+"_"+str(self.empnumber)
    
class Districtstaff(models.Model):
    GENDER = [['M', 'Male'],['F', 'Female']]
    STATUS = (('Registred', 'Registered'),('Updated', 'Updated'))
    fname = models.CharField("First Name",max_length=20)
    lname = models.CharField("Last Name",max_length=20)
    mname = models.CharField("Middle Name",max_length=20,blank=True)
    gender = models.CharField("Gender",choices=GENDER,max_length=1,null=True)
    isconfirmed = models.BooleanField(default=False)
    empnumber = models.CharField("Employee No.",unique=True,null=True,max_length=8)
    email = models.EmailField("Email",null=True,unique=True)
    mobile=models.CharField("Contact No.", max_length=20,blank=True,null=True,unique=True)
    nrc = models.CharField("NRC",max_length=11,null=True)
    birth_date = models.DateField("Date of Birth", auto_now=False, null=True)
    first_appointment = models.DateField("Date of First Appointment", auto_now=False, null=True)
    title = models.ForeignKey(Title,null=True,on_delete=models.SET_NULL)
    position = models.ForeignKey(Position,null=True,on_delete=models.SET_NULL)
    district = models.ForeignKey(District,on_delete=models.DO_NOTHING)
    province = models.ForeignKey(Province,on_delete=models.DO_NOTHING)
    datecreated= models.DateTimeField(auto_now_add=True)
    status = models.CharField("STATUS",choices=STATUS,max_length=11,default="Registered")
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    search = models.CharField("Search",max_length=200,null=True)
    export_to_file=models.BooleanField(default=False)
    is_updated=models.BooleanField(default=False)
    profilepic=models.ImageField("Staff Photo",upload_to='profile',default="profile/profile.jpg")

    def __str__(self):
        return self.fname +" "+self.lname+"_"+str(self.empnumber)
    
    
class Provincialstaff(models.Model):
    GENDER = (('M', 'Male'),('F', 'Female'))
    STATUS = (('Registred', 'Registered'),('Updated', 'Updated'))
    fname = models.CharField("First Name",max_length=20)
    lname = models.CharField("Last Name",max_length=20)
    mname = models.CharField("Middle Name",max_length=20,blank=True)
    gender = models.CharField("Gender",choices=GENDER,max_length=1,null=True)
    isconfirmed = models.BooleanField(default=False)
    empnumber = models.CharField("Employee No.",unique=True,null=True,max_length=15)
    email = models.EmailField("Email",null=True,unique=True)
    mobile=models.CharField("Contact No.", max_length=20,blank=True,null=True,unique=True)
    nrc = models.CharField("NRC",max_length=11,null=True)
    birth_date = models.DateField("Date of Birth", auto_now=False, null=True)
    first_appointment = models.DateField("Date of First Appointment", auto_now=False, null=True)
    title = models.ForeignKey(Title,null=True,on_delete=models.SET_NULL)
    position = models.ForeignKey(Position,null=True,on_delete=models.SET_NULL)
    province = models.ForeignKey(Province,on_delete=models.DO_NOTHING)
    datecreated= models.DateTimeField(auto_now_add=True)
    status = models.CharField("STATUS",choices=STATUS,max_length=11,default="Registered")
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    search = models.CharField("Search",max_length=200,null=True)
    export_to_file=models.BooleanField(default=False)
    is_updated=models.BooleanField(default=False)
    profilepic=models.ImageField("Staff Photo",upload_to='profile',default="profile/profile.jpg")

    def __str__(self):
        return self.fname +" "+self.lname+"_"+str(self.empnumber)
    

