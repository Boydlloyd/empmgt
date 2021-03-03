from django.db import models
from django.contrib.auth.models import User
from staff.models import Staff
import datetime
# Create your models here.

class Qualificationmodule(models.Model):
    datecreated= models.DateTimeField(auto_now_add=True)
    
class Myqualification(models.Model):
    datecreated= models.DateTimeField(auto_now_add=True)    

class Mydocument(models.Model):
    datecreated= models.DateTimeField(auto_now_add=True) 
      
class Category(models.Model):
    category = models.CharField("Category of Study",max_length=30,unique=True)
    datecreated= models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.category 
    
class Categorylevel(models.Model):
    level = models.CharField("Level of Study",max_length=30,unique=True)
    datecreated= models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.level   
    
    
class Qualification(models.Model):
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    level = models.ForeignKey(Categorylevel,on_delete=models.DO_NOTHING)
    field = models.CharField("Field of Study",max_length=20,blank=True)
    #empnumber = models.Integer(default=0)
    documents = models.IntegerField(default=0)
    staff = models.ForeignKey(Staff,on_delete=models.DO_NOTHING)
    institute = models.CharField("Institution", max_length=50)
    date_started = models.DateField("Commencement Date", auto_now=False, null=True)
    date_completed = models.DateField("Completion Date", auto_now=False, null=True)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    search = models.CharField("Search",max_length=200,null=True)
    key=models.IntegerField(default=0)
    export_to_file=models.BooleanField(default=False)
    datecreated= models.DateTimeField(auto_now_add=True)
    is_uploaded=models.BooleanField(default=False)

    def __str__(self):
        return self.field
    
    
class Documentupload(models.Model):
    STATUS = (('Uploaded', 'Uploaded'),('Submitted', 'Submitted'),('Accepted', 'Accepted'),('Rejected', 'Rejected'))
    qualification = models.ForeignKey(Qualification,on_delete=models.DO_NOTHING)
    staff = models.ForeignKey(Staff,on_delete=models.DO_NOTHING)
    documentupload=models.FileField("Upload Document",upload_to='uploads')
    doctitle = models.CharField("Document Title", max_length=100)
    docname = models.CharField(max_length=100,default="")
    status = models.CharField("Status",choices=STATUS,max_length=10,default="Uploaded")
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    isimage=models.BooleanField(default=True)
    key=models.IntegerField(default=0)
    datecreated= models.DateTimeField(auto_now_add=True)
    
class Maindocument(models.Model):
    docttype = models.CharField("Document Type", max_length=100)
    description = models.CharField(max_length=100,default="")
    documents = models.IntegerField(default=0)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    datecreated= models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.docttype
    
        
class Staffdocument(models.Model):
    STATUS = (('Uploaded', 'Uploaded'),('Submitted', 'Submitted'),('Accepted', 'Accepted'),('Rejected', 'Rejected'))
    document = models.ForeignKey(Maindocument,on_delete=models.DO_NOTHING)
    staff = models.ForeignKey(Staff,on_delete=models.DO_NOTHING)
    documentupload=models.FileField("Upload Document",upload_to='uploads')    
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    docname = models.CharField(max_length=100,default="")
    status = models.CharField("Status",choices=STATUS,max_length=10,default="Uploaded")
    isimage=models.BooleanField(default=True)
    datecreated= models.DateTimeField(auto_now_add=True)
    is_uploaded=models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.document.id)
    
