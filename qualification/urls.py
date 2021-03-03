from django.urls import path
from qualification import views

urlpatterns=[
    #======================MYQUALIFICATIONS========================================
    
    path('qualification/addmyqualification', views.add_myqualification,name='addmyqualification'),
    path('qualification/myqualifications', views.my_qualification,name='myqualifications'),
    path('qualification/deletemyqualification/<int:id>', views.delete_myqualification,name='deletemyqualification'),
    path('qualification/updatemyqualification/<int:id>', views.update_myqualification,name='updatemyqualification'),
        
    #======================STAFF QUALIFICATIONS========================================
    path('qualification/qualification', views.qualication_module,name='qualicationmodule'),
    path('qualification/addqualification/<int:id>', views.add_qualification,name='addqualification'),
    path('qualification/allqualifications', views.all_qualifications,name='allqualifications'),
    
    #======================CATEGORY LEVEL========================================
    path('qualification/createcategorylevel', views.create_categorylevel,name='createcategorylevel'),
    path('qualification/categorylevels', views.category_levels,name='categorylevels'),
    path('qualification/deletecategorylevel/<int:id>', views.delete_categorylevel,name='deletecategorylevel'),
    
    
    #======================CATEGORIES========================================
    path('qualification/createcategory', views.create_category,name='createcategory'),
    path('qualification/allcategories', views.all_categories,name='allcategories'),
    path('qualification/updatecategory/<int:id>', views.update_category,name='updatecategory'),
    path('qualification/deletequalification/<int:id>', views.delete_qualification,name='deletequalification'),
    
    
    
    
    
    #======================MAIN DOCUMENTS========================================
    path('document/createmaindocument', views.create_maindocument,name='createmaindocument'),
    path('document/allmaindocuments', views.all_maindocuments,name='allmaindocuments'),
    path('document/updatemaindocument/<int:id>', views.update_maindocument,name='updatemaindocument'),
    path('document/uploadmaindocument/<int:id>', views.upload_maindocument,name='uploadmaindocument'),
   
    
    #======================MYUPLOADS========================================
    path('document/uploadmydocument/<int:id>', views.upload_mydocument,name='uploadmydocument'),
    path('document/mydocuments', views.my_documents,name='mydocuments'),
    path('document/myuploads/<int:id>', views.my_uploads,name='myuploads'),
    path('document/updatemydocument/<int:id>', views.update_mydocument,name='updatemydocument'),
    path('document/deletemyupload/<int:id>', views.delete_myupload,name='deletemyupload'),  
    path('document/deletemymainupload/<int:id>', views.delete_mymainupload,name='deletemymainupload'),  
    
    
	
]