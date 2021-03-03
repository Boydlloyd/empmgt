from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import User,Group,Permission
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.db import connection
from .filters import *
import datetime
from django.contrib.auth.hashers import make_password

from django.contrib.auth.decorators import permission_required
# Create your views here.

from django.utils import six
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

def permission_required(perm, login_url=None, raise_exception=True):
	def check_perms(user):
		if isinstance(perm, six.string_types):
			perms = (perm, )
		else:
			perms = perm
		if user.has_perms(perms):
			return True
		if raise_exception and user.pk:
			raise PermissionDenied
		return False
	return user_passes_test(check_perms, login_url=login_url)


def action_time():
	current = datetime.datetime.now()
	year=current.strftime("%y")
	month=current.strftime("%m")
	day=current.strftime("%d")
	hour=current.strftime("%H")
	minute=current.strftime("%M")
	sec=current.strftime("%S")
	action_time=year+"-"+month+"-"+day+" "+hour+":"+minute+":"+sec
	return action_time

def write_to_file(user,message,key):
	file = open("file/"+str(user)+".json","a") 
	text=str(action_time())+" :"+str(message)+ " key="+str(key)+"\n"
	file.write(str(text))
	file.close() 

@permission_required('account.view_usermodule')		
def user_module(request):
	context={"title":"Users","showform":"none",}
	return render(request,'module.html',context)

def user_login(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method=="POST":
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(username=username.lower(),password=password)
		if user is not None:
			login(request,user)
			logged_user=User.objects.get(username=username.lower())
			write_to_file(request.user,"Logged in "+username.lower(),username.lower())
			messages.success(request, "Welcome "+logged_user.first_name+":"+str(username.lower()))
			return redirect('/')
		else:
			write_to_file(request.user,"Incorrect Credentials",username.lower())
			messages.error(request, "Incorrect Credentials")
	context={"title":"Employee Management System"}
	return render(request,'login.html',context)


def user_logout(request):
	write_to_file(request.user,"Logged out",request.user)
	logout(request)
	return redirect('/userlogin')

def home(request):
	if request.user.is_authenticated:
		role_count_teacher = Group.objects.filter(name="Teacher").count()
		role_count_du = Group.objects.filter(name="District_User").count()
		role_count_pu = Group.objects.filter(name="Provincial_User").count()
		role_count_nu = Group.objects.filter(name="National_User").count()
		role_count_sthr = Group.objects.filter(name="Station_HR").count()
		role_count_duhr = Group.objects.filter(name="District_HR").count()
		role_count_puhr = Group.objects.filter(name="Provincial_HR").count()
		role_count_nuhr = Group.objects.filter(name="National_HR").count()
		role_count_admin = Group.objects.filter(name="Admin").count()
		if role_count_admin==0:
			Group.objects.create(name="Admin")
			role=Group.objects.get(name="Admin")
			cursor=connection.cursor()
			rawsql="INSERT INTO auth_group_permissions (group_id,permission_id) VALUES ('"+str(role.id)+"',1)"
			cursor.execute(rawsql)
		else:
			pass
		if role_count_teacher==0:
			Group.objects.create(name="Teacher")
			role=Group.objects.get(name="Teacher")
			cursor=connection.cursor()
			rawsql="INSERT INTO auth_group_permissions (group_id,permission_id) VALUES ('"+str(role.id)+"',1)"
			cursor.execute(rawsql)
		else:
			pass
		if role_count_du==0:
			Group.objects.create(name="District_User")
			role=Group.objects.get(name="District_User")
			cursor=connection.cursor()
			rawsql="INSERT INTO auth_group_permissions (group_id,permission_id) VALUES ('"+str(role.id)+"',1)"
			cursor.execute(rawsql)
		else:
			pass
		if role_count_pu==0:
			Group.objects.create(name="Provincial_User")
			role=Group.objects.get(name="Provincial_User")
			cursor=connection.cursor()
			rawsql="INSERT INTO auth_group_permissions (group_id,permission_id) VALUES ('"+str(role.id)+"',1)"
			cursor.execute(rawsql)
		else:
			pass
		if role_count_sthr==0:
			Group.objects.create(name="Station_HR")
			role=Group.objects.get(name="Station_HR")
			cursor=connection.cursor()
			rawsql="INSERT INTO auth_group_permissions (group_id,permission_id) VALUES ('"+str(role.id)+"',1)"
			cursor.execute(rawsql)
		else:
			pass
		if role_count_duhr==0:
			Group.objects.create(name="District_HR")
			role=Group.objects.get(name="District_HR")
			cursor=connection.cursor()
			rawsql="INSERT INTO auth_group_permissions (group_id,permission_id) VALUES ('"+str(role.id)+"',1)"
			cursor.execute(rawsql)
		else:
			pass
		if role_count_puhr==0:
			Group.objects.create(name="Provincial_HR")
			role=Group.objects.get(name="Provincial_HR")
			cursor=connection.cursor()
			rawsql="INSERT INTO auth_group_permissions (group_id,permission_id) VALUES ('"+str(role.id)+"',1)"
			cursor.execute(rawsql)
		else:
			pass
		if role_count_nuhr==0:
			Group.objects.create(name="National_HR")
			role=Group.objects.get(name="National_HR")
			cursor=connection.cursor()
			rawsql="INSERT INTO auth_group_permissions (group_id,permission_id) VALUES ('"+str(role.id)+"',1)"
			cursor.execute(rawsql)
		else:
			pass
		if role_count_nu==0:
			Group.objects.create(name="National_User")
			role=Group.objects.get(name="National_User")
			cursor=connection.cursor()
			rawsql="INSERT INTO auth_group_permissions (group_id,permission_id) VALUES ('"+str(role.id)+"',1)"
			cursor.execute(rawsql)
		else:
			pass
		context={"title":"Employee Management System","showform":"none"}
		return render(request,'home.html',context)
	else:
		return redirect('/userlogin')



@permission_required('account.view_setupmodule')
def setup(request):
	showform='none'
	context={"title":"Setup","showform":showform}
	return render(request,'module.html',context)


def change_password(request):
	if request.method=='POST':
		form=PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, "Password has been reset successfully!")
			write_to_file(request.user,"Password has been reset successfully!",request.user)
			return redirect('/')
		else:
			return redirect('/account/changepassword')
	else:
		form=PasswordChangeForm(user=request.user)
	context={"title":"Reset My Password","form":form}
	return render(request,'account/changepassword.html',context)

@permission_required('auth.add_user')
def create_user(request):
	form=CreateNewuser(request.POST or None)
	roles=Group.objects.all()
	if form.is_valid():
		newForm=form.save(commit=False)
		if username_validated(request,newForm.userid) and phone_validated(request,newForm.mobile):
			insert_into_user(newForm.userid.lower(),newForm.fname,newForm.lname,newForm.email,False,newForm.mobile)
			newForm.userid.lower()
			newForm.save()
			user=User.objects.latest('id')
			roleid=request.POST.get('roleid')	
			user_group = Group.objects.get(id=roleid) 
			user_group.user_set.add(user.id)
			insert_into_userhistory(user.id,newForm.fname,newForm.lname,newForm.email,True,user.last_login,user.date_joined,user_group,request.user)
			assign_access_level(user.id,0,1,"National User")
			messages.success(request, "User Created successfully!")
			write_to_file(request.user,"User Created successfully!",user.id)
			return redirect('/user/allusers')
	context={"title":"Create User","form":form,"roles":roles}
	return render(request,'user/createuser.html',context)


def user_register(request):
	form=RegisterNewuser(request.POST or None)
	if form.is_valid():
		newForm=form.save(commit=False)
		if username_validated(request,newForm.userid) and phone_validated(request,newForm.mobile):
			if newForm.password1==newForm.password2:
				insert_into_user(newForm.userid.lower(),newForm.fname,newForm.lname,newForm.email,False,newForm.password1)
				newForm.userid.lower()
				newForm.save()
				user=User.objects.latest('id')
				gender=request.POST.get('gender')		
				insert_into_station_staff(newForm.fname,newForm.lname,newForm.mobile,newForm.email,gender,user.id)
				register_userhistory(user.id,newForm.fname,newForm.lname,newForm.email,user.last_login,user.date_joined)
				staff=Staff.objects.latest('id')
				assign_access_level(user.id,staff.id,4,"Station User")
				user_group = Group.objects.get(name="Teacher") 
				user_group.user_set.add(user.id)
				new_user=Newuser.objects.latest('id')
				Newuser.objects.filter(id=new_user.id).update(userid=newForm.userid.lower(),password1=make_password(newForm.password1),password2=make_password(newForm.password1))
				Staff.objects.filter(id=staff.id).update(search=user.username+" "+staff.fname+" "+staff.lname+" "+staff.mobile+" "+user.email)
				messages.success(request, "Congratulations "+str(newForm.fname)+", You have Registered successfully!")
				write_to_file(request.user,"User Registered successfully!",user.id)
				return redirect('/userlogin')
			else:
				messages.warning(request, "Passwords do not match")
	teacher=Group.objects.filter(name="Teacher").count()
	context={"title":"User Registration","form":form,}
	if teacher>0:
		return render(request,'user/userregister.html',context)
	else:
		Group.object.create(name="Teacher")
		return render(request,'user/userregister.html',context)

    
def phone_validated(request,phone):
	length_count=Mobilelength.objects.filter(length=len(phone)).count()
	if length_count>0:
		mformat1=phone[0:3]
		mformat2=phone[0:4]
		mformat3=phone[0:5]
		mformat4=phone[0:6]
		format_count1=Mobileformat.objects.filter(mformat=mformat1).count()
		format_count2=Mobileformat.objects.filter(mformat=mformat2).count()
		format_count3=Mobileformat.objects.filter(mformat=mformat3).count()
		format_count4=Mobileformat.objects.filter(mformat=mformat4).count()
		if int(format_count1)>0 or int(format_count2)>0 or int(format_count3)>0 or int(format_count4)>0:
			if (phone[1:len(phone)]).isdigit():
				#messages.success(request, "Coooool Phone")
				return True
			else:
				#messages.error(request, "Invalid Character typed in Phone number [" +str(phone)+"]")
				messages.error(request, "Invalid Character typed in Phone number [" +str(phone[1:len(phone)])+"]")
				return False
		else:
			messages.error(request, "Invalid Mobile Phone number format")
			return False
	else:
		messages.error(request, "Invalid Lenght for Mobile Phone number")
	return False

def username_validated(request,username):
	if ' ' in username:
		messages.warning(request, "Username should not contain spaces")
	else:
		user_count=User.objects.filter(username=username.lower()).count()
		if int(user_count)==0:
			#messages.success(request, "Coooool Username")
			return True
		else:
			messages.error(request, "Username "+username+" is already in use")
			return False
	return False    

def user_validate(request,level,userid):
    if level==1:
        return True
    if level==2:
        staff=Provincialstaff.objects.get(id=userid)
        if staff.is_updated==True:
            return True
        else:
            messages.warning(request, "Please Update Your Profile")
            return False
    elif level==3:
        staff=Districtstaff.objects.get(id=userid)
        if staff.is_updated==True:
            return True
        else:
            messages.warning(request, "Please Update Your Profile")
            return False
    elif level==4:
        staff=Staff.objects.get(id=userid)
        if staff.is_updated==True:
            return True
        else:
            messages.warning(request, "Please Update Your Profile")
            return False


@permission_required('auth.add_group')
def create_role(request):
	form=RoleForm(request.POST or None)
	if form.is_valid():
		form.save()
		role=Group.objects.latest('id')
		cursor=connection.cursor()
		rawsql="INSERT INTO auth_group_permissions (group_id,permission_id) VALUES ('"+str(role.id)+"',1)"
		cursor.execute(rawsql)
		messages.success(request, "Role Created successfully!")
		write_to_file(request.user,str(role)+ " Role Created successfully!",role.id)
		return redirect('/user/userroles')
	context={"title":"Create Role","form":form,}
	return render(request,'user/create.html',context)


@permission_required('auth.change_group')
def update_role(request,id=None):
	record = get_object_or_404(Group, id=id)
	form = RoleForm(request.POST or None, instance=record)
	if form.is_valid():
		form.save()
		messages.success(request, "Role Updated successfully!")
		write_to_file(request.user,"Role Updated successfully!",record.id)
		return redirect('/user/userroles')
	context = {"title": 'Update Role',"record": record,"form": form,}
	return render(request,'user/create.html',context)


@permission_required('auth.change_user')
def edit_user(request,id=None):
	record = get_object_or_404(User, id=id)
	form=UserCreationForm(request.POST or None, instance=record)
	form.fields['username'].widget = forms.HiddenInput()
	roles = Group.objects.all()
	cursor=connection.cursor()
	rawsql="SELECT auth_user.id,auth_user_groups.group_id FROM auth_user JOIN auth_user_groups ON auth_user.id=auth_user_groups.user_id WHERE auth_user.id='"+str(record.id)+"'"
	cursor.execute(rawsql)
	result=cursor.fetchall()
	for myrole in result:
		pass
	rol=Group.objects.get(id=myrole[1])
	context={"title":"Update User " +str(record.username),"form":form,"record":record,"roles":roles,"rol":rol}
	return render(request,'user/updateuser.html',context)


@permission_required('auth.change_user')
def update_user(request,id):
	record = get_object_or_404(User, id=id)
	fname=request.POST.get('fname')
	lname=request.POST.get('lname')
	email=request.POST.get('email')
	role=request.POST.get('role')
	active=bool(request.POST.get('active'))
	User.objects.filter(id=record.id).update(first_name=fname, last_name=lname,email=email,is_active=active)
	insert_into_userhistory(record.id,fname,lname,email,active,record.last_login,record.date_joined,role,request.user)
	user_role=Group.objects.get(name=role)
	cursor=connection.cursor()
	rawsql="UPDATE auth_user_groups SET group_id='"+str(user_role.id)+"' WHERE user_id='"+str(record.id)+"'"
	cursor.execute(rawsql)
	messages.success(request, "User Updated successfully!")
	write_to_file(request.user,"User Updated successfully!",record.id)
	return redirect('/user/allusers')


def reset_user_password(request,id):
	record = get_object_or_404(User, id=id)
	newuser=Newuser.objects.get(userid=record.username)
	record.password=make_password(newuser.mobile)
	record.save()
	messages.success(request, "User Password Reset successfully!")
	write_to_file(request.user,"User Password Reset successfully!",record.id)
	return redirect('/user/allusers')

@permission_required('auth.view_user')
def all_users(request):
	records=User.objects.filter(is_superuser=False).order_by('-id')
	totalrecords=User.objects.filter(is_superuser=False).count()
	filtered=records.count()
	myFilter=UserFilter(request.POST,queryset=records)
	records=myFilter.qs
	paginator=Paginator(records,20)
	page_num=request.GET.get('page', 1)
	records=paginator.get_page(page_num)
	pagecount=int(len(list(records)))
	counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
	roles=Group.objects.all().count()
	context={"title":"All Users","records":records,"allusers":"active","counted":counted,"myFilter":myFilter,}
	return render(request,'user/allusers.html',context)


@permission_required('auth.view_group')
def user_roles(request):
	records=Group.objects.all()
	totalrecords=Group.objects.all().count()
	filtered=records.count()
	paginator=Paginator(records,20)
	page_num=request.GET.get('page', 1)
	records=paginator.get_page(page_num)
	pagecount=int(len(list(records)))
	counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
	context={"title":"User Roles","records":records,"userroles":"active","counted":counted,"showform":"none",}
	return render(request,'user/userroles.html',context)

@permission_required('auth.view_permission')
def user_permissions(request):
	records=Permission.objects.all()
	totalrecords=Permission.objects.all().count()
	myFilter=PermissionFilter(request.POST,queryset=records)
	records=myFilter.qs
	filtered=records.count()
	paginator=Paginator(records,20)
	page_num=request.GET.get('page', 1)
	records=paginator.get_page(page_num)
	pagecount=int(len(list(records)))
	counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
	context={"title":"User Permissions","records":records,"userpermissions":"active","counted":counted,"myFilter":myFilter,}
	return render(request,'user/allpermissions.html',context)

@permission_required('auth.view_permission')
def role_permissions(request,id):
	record = get_object_or_404(Group, id=id)
	search=request.GET.get('search')
	cursor=connection.cursor()
	if search is None or search=="":
		rawsql="SELECT auth_group_permissions.id,auth_permission.id,app_label,model,codename,name FROM auth_group_permissions JOIN auth_permission ON auth_group_permissions.permission_id=auth_permission.id JOIN django_content_type ON auth_permission.content_type_id=django_content_type.id WHERE group_id ='"+str(record.id)+"'"
	else:
		rawsql="SELECT auth_group_permissions.id,auth_permission.id,app_label,model,codename,name FROM auth_group_permissions JOIN auth_permission ON auth_group_permissions.permission_id=auth_permission.id JOIN django_content_type ON auth_permission.content_type_id=django_content_type.id WHERE group_id ='"+str(record.id)+"' AND app_label='"+str(search)+"'"
	cursor.execute(rawsql)
	records=cursor.fetchall()
	rawsql2="SELECT COUNT(auth_group_permissions.id) FROM auth_group_permissions JOIN auth_permission ON auth_group_permissions.permission_id=auth_permission.id JOIN django_content_type ON auth_permission.content_type_id=django_content_type.id WHERE group_id ='"+str(record.id)+"'"
	cursor.execute(rawsql2)
	totalrecords=cursor.fetchall()
	for total in totalrecords:
		pass
	paginator=Paginator(records,total[0])
	page_num=request.GET.get('page', 1)
	records=paginator.get_page(page_num)
	pagecount=int(len(list(records)))
	counted=str(pagecount) +" out of "+str(total[0])+" record(s)"
	rawsqlapps="SELECT DISTINCT app_label FROM auth_group_permissions JOIN auth_permission ON auth_group_permissions.permission_id=auth_permission.id JOIN django_content_type ON auth_permission.content_type_id=django_content_type.id WHERE group_id ='"+str(record.id)+"'"
	cursor.execute(rawsqlapps)
	apps=cursor.fetchall()
	context={"title":"Permissions: "+str(record.name),"records":records,"apps":apps,"roleid":record.id,"role":record.name,"userpermissions":"active","addperm":"none","counted":counted,"total":total[0],"showform":"none",}
	return render(request,'user/rolepermissions.html',context)


@permission_required('auth.view_permission')
def manage_permissions(request,id):
	record = get_object_or_404(Group, id=id)
	cursor=connection.cursor()
	search=request.GET.get('search')
	cursor=connection.cursor()
	if search is None or search=="":
		rawsql="SELECT auth_permission.id,auth_permission.id,app_label,model,codename,name FROM auth_permission JOIN django_content_type ON auth_permission.content_type_id=django_content_type.id WHERE auth_permission.id NOT IN (SELECT permission_id FROM auth_group_permissions WHERE group_id='"+str(record.id)+"')"
	else:
		rawsql="SELECT auth_permission.id,auth_permission.id,app_label,model,codename,name FROM auth_permission JOIN django_content_type ON auth_permission.content_type_id=django_content_type.id WHERE app_label='"+str(search)+"' AND auth_permission.id NOT IN (SELECT permission_id FROM auth_group_permissions WHERE group_id='"+str(record.id)+"')"
	cursor.execute(rawsql)
	records=cursor.fetchall()

	rawsql2="SELECT COUNT(auth_permission.id) FROM auth_permission JOIN django_content_type ON auth_permission.content_type_id=django_content_type.id WHERE auth_permission.id NOT IN (SELECT permission_id FROM auth_group_permissions WHERE group_id='"+str(record.id)+"')"
	cursor.execute(rawsql2)
	totalrecords=cursor.fetchall()
	for total in totalrecords:
		pass
	paginator=Paginator(records,total[0])
	page_num=request.GET.get('page', 1)
	records=paginator.get_page(page_num)
	pagecount=int(len(list(records)))
	counted=str(pagecount) +" out of "+str(total[0])+" record(s)"
	rawsqlapps="SELECT DISTINCT app_label FROM auth_permission JOIN django_content_type ON auth_permission.content_type_id=django_content_type.id WHERE auth_permission.id NOT IN (SELECT permission_id FROM auth_group_permissions WHERE group_id='"+str(record.id)+"')"
	cursor.execute(rawsqlapps)
	apps=cursor.fetchall()
	context={"title":"Permissions: "+str(record.name),"records":records,"apps":apps,"roleid":record.id,"role":record.name,"userpermissions":"active","removeperm":"none","counted":counted,"total":total[0],"rawsql":rawsql,"showform":"none",}
	return render(request,'user/managepermissions.html',context)


@permission_required('auth.delete_permission')
def remove_permission(request):
	roleid=request.POST.get('roleid')
	keys=request.POST.getlist('id')
	cursor=connection.cursor()
	i=0
	for permid in keys:
		i+=1
		rawsql="DELETE FROM auth_group_permissions WHERE id='"+str(permid)+"' AND permission_id!=1"
		cursor.execute(rawsql)
		write_to_file(request.user,"Permission Removed from "+str(roleid),permid)
	if i==0:
		messages.warning(request,"No Permissions Selected for removal!")
		write_to_file(request.user,"No Permissions Selected!",0)
	elif i==1:
		messages.success(request, str(i) +" Permission removed successfully!")
	else:
		messages.success(request, str(i) +" Permissions removed successfully!")
	return redirect('/user/rolepermissions/'+str(roleid))

@permission_required('auth.add_permission')
def add_permission(request):
	roleid=request.POST.get('roleid')
	keys=request.POST.getlist('id')
	cursor=connection.cursor()
	i=0
	for permid in keys:
		i+=1
		rawsql="INSERT INTO auth_group_permissions (group_id,permission_id) VALUES ('"+str(roleid)+"','"+str(permid)+"')"
		cursor.execute(rawsql)
		write_to_file(request.user,"Permission Added to "+str(roleid),permid)
	if i==0:
		messages.warning(request,"No Permissions Selected for addition!")
	elif i==1:
		messages.success(request, str(i) +" Permission added successfully!")
	else:
		messages.success(request, str(i) +" Permissions added successfully!")
	return redirect('/user/managepermissions/'+str(roleid))

@permission_required('account.view_userhistory')
def user_audit(request,id):
	record = get_object_or_404(User, id=id)
	records=UserHistory.objects.filter(username=record.id).order_by('id')
	totalrecords=UserHistory.objects.filter(username=record.id).count()
	paginator=Paginator(records,20)
	page_num=request.GET.get('page', 1)
	records=paginator.get_page(page_num)
	pagecount=int(len(list(records)))
	counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
	context={"title":"User History ("+ str(record.username)+")","records":records,"counted":counted,"showform":"none",}
	return render(request,'user/userhistory.html',context)


@permission_required('account.view_useractivity')
def user_activity(request,id):
	record = get_object_or_404(User, id=id)
	file = open("./file/"+str(record.username)+".json","r") 
	records=file.read()
	file.close()
	context={"title":"User Activity: "+str(record.username),"file_content":records,"showform":"none",}
	return render(request,'user/useractivity.html',context)

@permission_required('account.add_serviceprovider')
def create_provider(request):
	form=ProviderForm(request.POST or None)
	if form.is_valid():
		form.save()
		provider=Serviceprovider.objects.latest('id')
		messages.success(request, "Service Provider Created successfully!")
		write_to_file(request.user, " Service Provider Created successfully!",provider.id)
		return redirect('/phone/serviceproviders')
	context={"title":"Create Service Provider","form":form,}
	return render(request,'phone/create.html',context)


@permission_required('account.view_serviceprovider')
def service_providers(request):
	records=Serviceprovider.objects.all()
	totalrecords=Serviceprovider.objects.all().count()
	filtered=records.count()
	paginator=Paginator(records,20)
	page_num=request.GET.get('page', 1)
	records=paginator.get_page(page_num)
	pagecount=int(len(list(records)))
	counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
	context={"title":"Mobile Service Providers","records":records,"serviceproviders":"active","counted":counted,"showform":"none",}
	return render(request,'phone/serviceproviders.html',context)


@permission_required('account.change_serviceprovider')
def update_provider(request,id=None):
	record = get_object_or_404(Serviceprovider, id=id)
	form = ProviderForm(request.POST or None, instance=record)
	if form.is_valid():
		form.save()
		messages.success(request, "Service Provider Updated successfully!")
		write_to_file(request.user,"Service Provider Updated successfully!",record.id)
		return redirect('/phone/serviceproviders')
	context = {"title": 'Update Service Provider',"record": record,"form": form,}
	return render(request,'phone/update.html',context)


@permission_required('account.add_mobileformat')
def create_mobileformat(request):
	form=MobileformatForm(request.POST or None)
	if form.is_valid():
		form.save()
		mformat=Mobileformat.objects.latest('id')
		messages.success(request, "Mobile Format Created successfully!")
		write_to_file(request.user," Mobile Format Created successfully!",mformat.id)
		return redirect('/phone/phonesettings')
	context={"title":"Create Mobile Format","form":form,}
	return render(request,'phone/create.html',context)


@permission_required('account.view_mobileformat')
def phone_settings(request):
	records=Mobileformat.objects.all()
	totalrecords=Mobileformat.objects.all().count()
	filtered=records.count()
	paginator=Paginator(records,20)
	page_num=request.GET.get('page', 1)
	records=paginator.get_page(page_num)
	pagecount=int(len(list(records)))
	counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
	context={"title":"Mobile Formats","records":records,"phonesettings":"active","counted":counted,"showform":"none",}
	return render(request,'phone/phonesettings.html',context)

@permission_required('account.change_mobileformat')
def update_format(request,id=None):
	record = get_object_or_404(Mobileformat, id=id)
	form = MobileformatForm(request.POST or None, instance=record)
	if form.is_valid():
		form.save()
		messages.success(request, "Service Provider Updated successfully!")
		write_to_file(request.user,"Service Provider Updated successfully!",record.id)
		return redirect('/phone/phonesettings')
	context = {"title": 'Update Mobile',"record": record,"form": form,}
	return render(request,'phone/update.html',context)


def insert_into_user(userid,fname,lname,email,is_staff,password):
	new_user=User()
	new_user.username=userid.strip().lower()
	new_user.first_name=fname.strip()
	new_user.last_name=lname.strip()
	new_user.email=email.lower()
	new_user.is_active=True
	new_user.is_staff=is_staff
	new_user.password=make_password(password)
	new_user.save()
 
def assign_access_level(user,staff,level,description):
	access_level=Userlevel()
	access_level.user_id=user
	access_level.staff=staff
	access_level.level=level
	access_level.description=description
	access_level.save()
 
def insert_into_userhistory(username,fname,lname,email,is_active,last_login,date_joined,role,author):
	user_history=UserHistory()
	user_history.username=username
	user_history.fname=fname.strip()
	user_history.lname=lname.strip()
	user_history.email=email.lower().strip()
	user_history.role=role
	user_history.is_active=is_active
	user_history.last_login=last_login
	user_history.date_joined=date_joined
	user_history.author=author
	user_history.save()

def register_userhistory(username,fname,lname,email,last_login,date_joined):
	user_history=UserHistory()
	user_history.username=username
	user_history.fname=fname.strip()
	user_history.lname=lname.strip()
	user_history.email=email.lower().strip()
	user_history.role="Teacher"
	user_history.is_active=True
	user_history.last_login=last_login
	user_history.date_joined=date_joined
	user_history.author_id=username
	user_history.save()


def insert_into_station_staff(fname,lname,mobile,email,gender,author):
	staff=Staff()
	staff.fname=fname.strip()
	staff.lname=lname.strip()
	staff.mobile=mobile
	staff.email=email.lower().strip()
	staff.gender=gender
	staff.author_id=author
	staff.save()


#0977279948
#8771

#0954903472
#0211253438