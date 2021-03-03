from django.urls import path
from account import views
from django.contrib.auth import views as auth_views

urlpatterns=[
	#======================HOME========================================
	path('home/', views.home,name='home'),
	path('', views.home,name='home'),
	

	#======================LOGIN========================================
	path('userlogin', views.user_login,name='userlogin'),

	#======================SETUP========================================
	path('setup', views.setup,name='setup'),
	#======================USER========================================
	
	path('user/userregister', views.user_register,name='userregister'),
 
	path('user/user', views.user_module,name='user'),
	path('user/createuser', views.create_user,name='createuser'),
	path('user/edituser/<int:id>', views.edit_user,name='edituser'),
	path('user/updateuser/<int:id>', views.update_user,name='updateuser'),
	path('user/allusers', views.all_users,name='allusers'),
	path('user/useraudit/<int:id>', views.user_audit,name='useraudit'),
	
	path('user/useractivity/<int:id>', views.user_activity,name='useractivity'),
	path('user/userroles', views.user_roles,name='userroles'),
	path('user/updaterole/<int:id>', views.update_role,name='updaterole'),
	path('user/userpermissions', views.user_permissions,name='userpermissions'),
	path('user/managepermissions/<int:id>', views.manage_permissions,name='managepermissions'),
	path('user/rolepermissions/<int:id>', views.role_permissions,name='rolepermissions'),
	path('user/addpermission', views.add_permission,name='addpermission'),
	path('user/removepermission', views.remove_permission,name='removepermission'),
	path('user/createrole', views.create_role,name='createrole'),

	#======================PASSWORD RESET========================================
	path('account/changepassword', views.change_password,name='changepassword'),
	path('account/resetpassword/', auth_views.PasswordResetView.as_view(template_name="account/password_reset.html"),name='resetpassword'),
	path('account/resetpasswor_done/', auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_sent.html"),name='password_reset_done'),
	path('account/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_form.html"),name='reset'),
	path('account/resetpassword_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_done.html"),name='reset_password_complete'),

	#======================PHONE SETUP========================================
	path('phone/createprovider', views.create_provider,name='createprovider'),
	path('phone/serviceproviders', views.service_providers,name='serviceproviders'),
 	path('phone/updateprovider/<int:id>', views.update_provider,name='updateprovider'),
	
	path('phone/createmobileformat', views.create_mobileformat,name='createmobileformat'),
	path('phone/phonesettings', views.phone_settings,name='phonesettings'),
	path('phone/updateformat/<int:id>', views.update_format,name='updateformat'),
	
 	
	path('account/resetuserpassword/<int:id>', views.reset_user_password,name='resetuserpassword'),
	#======================LOGOUT========================================
	path('userlogout', views.user_logout,name='userlogout'),

	
]