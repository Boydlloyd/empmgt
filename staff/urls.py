from django.urls import path
from staff import views

urlpatterns=[
    #======================STAFF========================================
    path('staff/staff', views.staff_module,name='staffmodule'),
    path('staff/createstaff', views.create_staff,name='createstaff'),
    path('staff/unapprovedstaff', views.unapproved_staff,name='unapprovedstaff'),
    path('staff/allstaff', views.all_staff,name='allstaff'),
    path('staff/updatestaffbio/<int:id>', views.update_staff_bio,name='updatestaffbio'),
    path('staff/updatestaffwork/<int:id>', views.update_staff_work,name='updatestaffwork'),
    path('staff/updatestaffphoto/<int:id>', views.update_staffphoto,name='updatestaffphoto'),
    path('staff/approvestaff/<int:id>', views.approve_staff,name='approvestaff'),
    path('staff/disapprovestaff/<int:id>', views.disapprove_staff,name='disapprovestaff'),
    path('staff/initializestaff/<int:id>', views.initialize_staff,name='initializestaff'),
    
    
    #======================DISTRICT STAFF========================================
    path('staff/creatediststaff', views.create_dist_staff,name='creatediststaff'),
    path('staff/districtstaff', views.district_staff,name='districtstaff'),
    path('staff/updatediststaff/<int:id>', views.update_dist_staff,name='updatediststaff'),
    
    
    #======================PROVINCIAL STAFF========================================
    path('staff/createprovstaff', views.create_prov_staff,name='createprovstaff'),
    path('staff/provincialstaff', views.provincial_staff,name='provincialstaff'),
    path('staff/updateprovstaff/<int:id>', views.update_prov_staff,name='updateprovstaff'),
    
    
    #======================MYPROFILE========================================
    path('staff/myprofile', views.my_profile,name='myprofile'),
    path('staff/updatemybioprofile', views.update_mybio_profile,name='updatemybioprofile'),
    path('staff/updatemyworkprofile', views.update_mywork_profile,name='updatemyworkprofile'),    
    path('staff/updatemyphoto', views.update_myphoto,name='updatemyphoto'),
    path('staff/submitmyinfo', views.submit_myinfo,name='submitmyinfo'),
    path('staff/cancelmysubmission', views.cancel_mysubmission,name='cancelmysubmission'),
    path('staff/initializemyprofile', views.initialize_myprofile,name='initializemyprofile'),
    
    
    #======================MYPROFILE========================================
    path('staff/staffprofile/<int:id>', views.staff_profile,name='staffprofile'),
    
  
    #======================POSITION========================================
    path('staff/createposition', views.create_position,name='createposition'),
    path('staff/allpositions', views.all_positions,name='allpositions'),
    path('staff/updateposition/<int:id>', views.update_position,name='updateposition'),
   
    #======================TITLE========================================
    path('staff/createtitle', views.create_title,name='createtitle'),
    path('staff/alltitles', views.all_titles,name='alltitles'),
    path('staff/updatetitle/<int:id>', views.update_title,name='updatetitle'),
	
]