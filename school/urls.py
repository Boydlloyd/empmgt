from django.urls import path
from school import views

urlpatterns=[
    #======================SCHOOL========================================
    path('school/school', views.school_module,name='schoolmodule'),
     path('school/createschool', views.create_school,name='createschool'),
	path('school/allschools', views.all_schools,name='allschools'),
    path('school/updateschool/<int:id>', views.update_school,name='updateschool'),
    

    #======================PROVINCE========================================
    path('school/createprovince', views.create_province,name='createprovince'),
    path('school/allprovinces', views.all_provinces,name='allprovinces'),
    path('school/updatedistrict/<int:id>', views.update_district,name='updatedistrict'),  

    #======================DISTRICT========================================
    
    path('school/createdistrict/<int:id>', views.create_district,name='createdistrict'),
    path('school/alldistricts', views.all_districts,name='alldistricts'),
    path('school/updateprovince/<int:id>', views.update_province,name='updateprovince'),  
	
]