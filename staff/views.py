from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from account.views import insert_into_user,insert_into_userhistory,assign_access_level,insert_into_station_staff,phone_validated,username_validated,user_validate
from django.contrib import messages
from django.core.paginator import Paginator
from qualification.models import Documentupload,Staffdocument,Qualification,Maindocument
from .filters import *
import datetime
import random
from django.utils import six
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.hashers import make_password

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


@permission_required('staff.view_staffmodule')		
def staff_module(request):
    level=Userlevel.objects.get(user=request.user)
    if user_validate(request,level.level,level.staff):
        context={"title":"Members of Staff","showform":"none",}
        return render(request,'module.html',context)
    return redirect('/staff/staff')
    

@permission_required('staff.add_position')
def create_position(request):
    form=PositionForm(request.POST or None)
    if form.is_valid():
        newForm=form.save(commit=False)
        newForm.author=request.user
        newForm.save()
        position=Position.objects.latest('id')
        messages.success(request, "Position Created successfully!")
        write_to_file(request.user,"Position Created successfully!",position.id)
        return redirect('/staff/allpositions')
    context={"title":"Create Position","form":form,}
    return render(request,'staff/createposition.html',context)


@permission_required('staff.view_position')
def all_positions(request):
	records=Position.objects.all().order_by('-id')
	totalrecords=Position.objects.filter().count()
	filtered=records.count()
	paginator=Paginator(records,25)
	page_num=request.GET.get('page', 1)
	records=paginator.get_page(page_num)
	pagecount=int(len(list(records)))
	counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
	context={"title":"Staff Positions","records":records,"allpositions":"active","counted":counted,"showform":"none",}
	return render(request,'staff/allpositions.html',context)

@permission_required('staff.change_position')
def update_position(request,id=None):
    record = get_object_or_404(Position, id=id)
    form = PositionForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        messages.success(request, "District Updated successfully!")
        write_to_file(request.user,"District Updated successfully!",record.id)
        record.author=request.user
        record.save()
        return redirect('/staff/allpositions')
    context = {"title": 'Update Position',"record": record,"form": form,}
    return render(request,'staff/createposition.html',context)


@permission_required('staff.add_title')
def create_title(request):
    form=TitleForm(request.POST or None)
    if form.is_valid():
        newForm=form.save(commit=False)
        newForm.author=request.user
        newForm.save()
        return redirect('/staff/alltitles')
    context={"title":"Create Title","form":form,}
    return render(request,'staff/createtitle.html',context)


@permission_required('staff.view_title')
def all_titles(request):
	records=Title.objects.all().order_by('-id')
	totalrecords=Title.objects.filter().count()
	filtered=records.count()
	paginator=Paginator(records,10)
	page_num=request.GET.get('page', 1)
	records=paginator.get_page(page_num)
	pagecount=int(len(list(records)))
	counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
	context={"title":"Staff Titles","records":records,"alltitles":"active","counted":counted,"showform":"none",}
	return render(request,'staff/alltitles.html',context)


@permission_required('staff.change_title')
def update_title(request,id=None):
    record = get_object_or_404(Title, id=id)
    form = TitleForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        messages.success(request, "Title Updated successfully!")
        write_to_file(request.user,"Title Updated successfully!",record.id)
        record.author=request.user
        record.save()
        return redirect('/staff/alltitles')
    context = {"title": 'Update Title',"record": record,"form": form,}
    return render(request,'staff/createtitle.html',context)


@permission_required('staff.add_staff')
def create_staff(request):
    districts=District.objects.all()
    level=Userlevel.objects.get(user=request.user)
    if user_validate(request,level.level,level.staff):
        form=RegisterStaff(request.POST or None)
        if form.is_valid():
            newForm=form.save(commit=False)
            if username_validated(request,newForm.userid) and phone_validated(request,newForm.mobile):
                insert_into_user(newForm.userid.lower(),newForm.fname,newForm.lname,newForm.email,False,newForm.mobile)
                newForm.userid.lower()
                newForm.save()
                user=User.objects.latest('id')
                gender=request.POST.get('gender')
                user_role = Group.objects.get(name="Teacher") 
                user_role.user_set.add(user.id)
                insert_into_station_staff(newForm.fname,newForm.lname,newForm.mobile,newForm.email,gender,level.user_id)
                staff=Staff.objects.latest('id')
                insert_into_userhistory(user.id,newForm.fname,newForm.lname,newForm.email,True,user.last_login,user.date_joined,user_role,request.user)
                assign_access_level(user.id,staff.id,4,"Station User")
                if level.level==4:
                    creator=Staff.objects.get(id=level.staff)
                    Staff.objects.filter(id=staff.id).update(school_id=creator.school_id,district_id=creator.district_id,province_id=creator.province_id)
                    staffnumber=Staff.objects.filter(school_id=creator.school_id).count()
                    School.objects.filter(id=creator.school_id).update(staffnumber=staffnumber)
                    staffnumber=Staff.objects.filter(district_id=creator.district_id).count()
                    District.objects.filter(id=creator.district_id).update(staffnumber=staffnumber)
                    staffnumber=Staff.objects.filter(province_id=creator.province_id).count()
                    Province.objects.filter(id=creator.province_id).update(staffnumber=staffnumber)
                else:
                    district=request.POST.get('district')
                    dist=District.objects.get(id=district)
                    Staff.objects.filter(id=staff.id).update(district_id=district,province_id=dist.province_id,search=user.username+" "+staff.fname+" "+staff.lname+" "+staff.mobile+" "+user.email)
                    staffnumber=Staff.objects.filter(district_id=district).count()
                    District.objects.filter(id=district).update(staffnumber=staffnumber)
                    staffnumber=Staff.objects.filter(province_id=dist.province_id).count()
                    Province.objects.filter(id=dist.province_id).update(staffnumber=staffnumber)
                messages.success(request, "Staff Created successfully!")
                write_to_file(request.user,"Staff Created successfully!",staff.id)
                return redirect('/staff/allstaff')
        
        context={"title":"Create Staff Station","form":form,"level":level.level,"districts":districts}
        return render(request,'staff/createstaff.html',context)
    return redirect('/')


@permission_required('staff.view_staff')
def unapproved_staff(request):
    level=Userlevel.objects.get(user=request.user)
    if user_validate(request,level.level,level.staff):
        if level.level==1:
            records=Staff.objects.filter(status="Pending").order_by('-id')
            totalrecords=Staff.objects.filter(status="Pending").count()
            filtered=records.count()
            myFilter=StaffFilter(request.POST,queryset=records)
        elif level.level==2:
            staff=Provincialstaff.objects.get(id=level.staff)
            records=Staff.objects.filter(status="Pending",province_id=staff.province).order_by('-id')
            totalrecords=Staff.objects.filter(status="Pending",province_id=staff.province).count()
            filtered=records.count()
            myFilter=StaffFilter2(request.POST,queryset=records)
        elif level.level==3:
            staff=Districtstaff.objects.get(id=level.staff)
            records=Staff.objects.filter(status="Pending",district_id=staff.district).order_by('-id')
            totalrecords=Staff.objects.filter(status="Pending",district_id=staff.district).count()
            filtered=records.count()
            myFilter=StaffFilter3(request.POST,queryset=records)
        elif level.level==4:
            staff=Staff.objects.get(id=level.staff)
            records=Staff.objects.filter(status="Pending",school_id=staff.school_id).order_by('-id')
            totalrecords=Staff.objects.filter(status="Pending",school_id=staff.school_id).count()
            myFilter=StaffFilter4(request.POST,queryset=records)
        else:
            records=Staff.objects.none()
            totalrecords=0
            myFilter=StaffFilterNone(request.POST,queryset=records)
        filtered=records.count()
        records=myFilter.qs
        paginator=Paginator(records,20)
        page_num=request.GET.get('page', 1)
        records=paginator.get_page(page_num)
        pagecount=int(len(list(records)))
        counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
        context={"title":"Members of Staff","records":records,"unapprovedstaff":"active","counted":counted,"myFilter":myFilter,}
        return render(request,'staff/unapprovedstaff.html',context)
    return redirect('/')


@permission_required('staff.view_staff')
def all_staff(request):
    level=Userlevel.objects.get(user=request.user)
    if user_validate(request,level.level,level.staff):
        if level.level==1:
            records=Staff.objects.all().order_by('-id')
            allrecords=Staff.objects.all().order_by('-id')
            allrecords=str(allrecords).replace("[<",'')
            allrecords=allrecords.replace(">]",'')
            allrecords=allrecords.replace(">",'')
            allrecords=allrecords.replace("<",'')
            allrecords=allrecords.replace("Staff:",'')
            totalrecords=Staff.objects.all().count()
            filtered=records.count()
            myFilter=StaffFilter(request.POST,queryset=records)
        elif level.level==2:
            staff=Provincialstaff.objects.get(id=level.staff)
            records=Staff.objects.filter(province_id=staff.province_id).order_by('-id')
            totalrecords=Staff.objects.filter(province_id=staff.province_id).count()
            filtered=records.count()
            myFilter=StaffFilter2(request.POST,queryset=records)
        elif level.level==3:
            staff=Districtstaff.objects.get(id=level.staff)
            records=Staff.objects.filter(district_id=staff.district_id).order_by('-id')
            totalrecords=Staff.objects.filter(district_id=staff.district_id).count()
            filtered=records.count()
            myFilter=StaffFilter3(request.POST,queryset=records)
        elif level.level==4:
            staff=Staff.objects.get(id=level.staff)
            records=Staff.objects.filter(school_id=staff.school_id).order_by('-id')
            totalrecords=Staff.objects.filter(school_id=staff.school_id).count()
            myFilter=StaffFilter4(request.POST,queryset=records)
        else:
            records=Staff.objects.none()
            totalrecords=0
            myFilter=StaffFilterNone(request.POST,queryset=records)
        filtered=records.count()
        records=myFilter.qs
        paginator=Paginator(records,15)
        page_num=request.GET.get('page', 1)
        records=paginator.get_page(page_num)
        pagecount=int(len(list(records)))
        counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
        context={"title":"Members of Staff","records":records,"allstaff":"active","counted":counted,"myFilter":myFilter,}
        return render(request,'staff/allstaff.html',context)
    return redirect('/')


@permission_required('staff.change_staff')
def update_staff_bio(request,id=None):
    record = get_object_or_404(Staff, id=id)
    level=Userlevel.objects.get(user=request.user)
    if user_validate(request,level.level,level.staff):
        form = UpdateStaffBioForm(request.POST or None, instance=record)
        if record.is_updated:
            form.fields['district'].widget = forms.HiddenInput()
        if form.is_valid():
            newForm=form.save(commit=False)
            if phone_validated(request,newForm.mobile):
                dist=District.objects.get(id=newForm.district_id)
                newForm.province_id=dist.province_id
                if record.empnumber == None:
                     search=record.mobile+" "+newForm.lname+" "+newForm.fname+" "+record.email
                else:
                    search=record.mobile+" "+record.nrc+" "+record.empnumber+" "+newForm.tsnumber+" "+newForm.lname+" "+newForm.fname+" "+record.email
                newForm.search=search
                newForm.save()
                messages.success(request, "Staff Updated successfully!")
                write_to_file(request.user,"Staff Updated successfully!",record.id)
                record.author=request.user
                record.save()
                staffnumber=Staff.objects.filter(district_id=newForm.district_id).count()
                District.objects.filter(id=newForm.district_id).update(staffnumber=staffnumber)
                staffnumber=Staff.objects.filter(province_id=dist.province_id).count()
                Province.objects.filter(id=dist.province_id).update(staffnumber=staffnumber)
                return redirect('/staff/updatestaffwork/'+str(id))
        context = {"title": 'Update Staff Bio',"record": record,"form": form,"updatestaffbio":"active"}
        return render(request,'staff/updatestaff.html',context)
    return render('/')


@permission_required('staff.change_staff')
def update_staff_work(request,id=None):
    record = get_object_or_404(Staff, id=id)
    schools=School.objects.filter(district=record.district)
    level=Userlevel.objects.get(user=request.user)
    if user_validate(request,level.level,level.staff):
        form = UpdateStaffWorkForm(request.POST or None, instance=record)
        if form.is_valid():
            newForm=form.save(commit=False)
            if nrc_validated(request,newForm.nrc):
                newForm.school_id=request.POST.get('school')
                newForm.is_updated=True
                newForm.status="Updated"
                search=record.mobile+" "+newForm.nrc+" "+newForm.empnumber+" "+newForm.tsnumber+" "+newForm.lname+" "+newForm.fname+" "+record.email
                newForm.search=search
                newForm.save()
                messages.success(request, "Staff Updated successfully!")
                write_to_file(request.user,"Staff Updated successfully!",record.id)
                record.author=request.user
                record.save()
                staffnumber=Staff.objects.filter(school_id=request.POST.get('school')).count()
                School.objects.filter(id=request.POST.get('school')).update(staffnumber=staffnumber)
                staffnumber=Staff.objects.filter(district_id=record.district_id).count()
                District.objects.filter(id=record.district_id).update(staffnumber=staffnumber)
                staffnumber=Staff.objects.filter(province_id=record.province_id).count()
                Province.objects.filter(id=record.province_id).update(staffnumber=staffnumber)
                return redirect('/staff/allstaff')
        context = {"title": 'Update Staff Work',"record": record,"form": form,"updatestaffwork":"active","schools":schools}
        return render(request,'staff/updatestaff.html',context)
    return render('/')


@permission_required('staff.view_staff')
def staff_profile(request,id):
    record = get_object_or_404(Staff, id=id)
    profile=Staff.objects.get(id=record.id)
    
    qualifications=Qualification.objects.filter(staff_id=record.id).order_by('-id')
    
    uploads=Documentupload.objects.filter(staff_id=record.id).order_by('-isimage')
    docs=Staffdocument.objects.filter(staff_id=record.id)
    
    uploadcount=Documentupload.objects.filter(staff_id=record.id).order_by('-isimage').count()
    doccount=Staffdocument.objects.filter(staff_id=record.id).count()    
    if record.status == "Pending":
        context={"title":'Information',"sub":record.fname+" "+record.fname+"'s","profile":profile,"myprofile":"active","qualifications":qualifications,"uploads":uploads,"docs":docs,"uploadcount":uploadcount,"doccount":doccount,"showform":'none'}
    else:
        context={"title":'Profile',"sub":record.fname+" "+record.fname+"'s","profile":profile,"myprofile":"active","qualifications":qualifications,"uploads":uploads,"docs":docs,"uploadcount":uploadcount,"doccount":doccount,"showform":'none'}
    return render(request,'staff/staffprofile.html',context)
    
    

@permission_required('staff.change_staff')
def approve_staff(request,id=None):
    record = get_object_or_404(Staff, id=id)
    level=Userlevel.objects.get(user=request.user)
    if user_validate(request,level.level,level.staff):
        record.status="Approved"
        work_on_documents(record.id,"Approved")
        record.save()
        messages.success(request, "Staff Information Approved successfully!")
        write_to_file(request.user,"Staff Information Approved successfully!",record.id)
        return redirect('/staff/unapprovedstaff')
    return redirect('/')


@permission_required('staff.change_staff')
def initialize_staff(request,id=None):
    record = get_object_or_404(Staff, id=id)
    level=Userlevel.objects.get(user=request.user)
    if user_validate(request,level.level,level.staff):
        record.status="Registered"
        record.school=None
        record.district=None
        record.province=None
        record.is_updated=False
        record.save()
        staffnumber=Staff.objects.filter(school_id=record.school_id).count()
        School.objects.filter(id=record.school_id).update(staffnumber=staffnumber)
        staffnumber=Staff.objects.filter(district_id=record.district_id).count()
        District.objects.filter(id=record.district_id).update(staffnumber=staffnumber)
        staffnumber=Staff.objects.filter(province_id=record.province_id).count()
        Province.objects.filter(id=record.province_id).update(staffnumber=staffnumber)
        work_on_documents(record.id,"Uploaded")
        messages.success(request, "Staff Status Initialized successfully!")
        write_to_file(request.user,"Staff Status Initialized successfully!",record.id)
        return redirect('/staff/allstaff')
    return redirect('/')


@permission_required('staff.change_staff')
def disapprove_staff(request,id=None):
    record = get_object_or_404(Staff, id=id)
    form = DisapprovalForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        messages.success(request, "Staff Information Disapproved successfully!")
        write_to_file(request.user,"Staff Information Disapproved successfully!",record.id)
        record.author=request.user
        record.status="Disapproved"
        record.save()
        work_on_documents(record.id,"Uploaded")
        return redirect('/staff/unapprovedstaff')
    context = {"title": 'Disapprove '+str(record.fname)+" "+str(record.lname)+"'s Information","record": record,"form": form,}
    return render(request,'staff/disapprovetestaff.html',context)

@permission_required('staff.change_staff')
def update_staffphoto(request,id=None):
    record = get_object_or_404(Staff, id=id)
    form = UploadStaffPhoto(request.POST or None,request.FILES or None, instance=record)
    if form.is_valid():
        form.save()
        messages.success(request, "Staff Photo Updated successfully!")
        write_to_file(request.user,"Staff Photo Updated successfully!",record.id)
        record.author=request.user
        record.save()
        return redirect('/staff/allstaff')
    context = {"title": 'Update '+str(record.fname)+' '+str(record.lname)+"'s Photo","record": record,"form": form,"level":0}
    return render(request,'staff/uploadstaffphoto.html',context)


@permission_required('staff.add_districtstaff')
def create_dist_staff(request):
    districts=District.objects.all()
    level=Userlevel.objects.get(user=request.user)
    form=RegisterStaff(request.POST or None)
    if form.is_valid():
        newForm=form.save(commit=False)
        if username_validated(request,newForm.userid) and phone_validated(request,newForm.mobile):
            insert_into_user(newForm.userid.lower(),newForm.fname,newForm.lname,newForm.email,False,newForm.mobile)
            newForm.userid.lower()
            newForm.save()
            user=User.objects.latest('id')
            gender=request.POST.get('gender')
            user_role = Group.objects.get(name="District_User") 
            insert_into_userhistory(user.id,newForm.fname,newForm.lname,newForm.email,True,user.last_login,user.date_joined,user_role,request.user)
            user_role.user_set.add(user.id)
            if level.level==3:
                creator=Districtstaff.objects.get(id=level.staff)
                insert_into_district_staff(newForm.fname,newForm.lname,newForm.mobile,newForm.email,gender,creator.district_id,creator.province_id,level.user_id)                                    
            else:
                district=request.POST.get('district')
                dist=District.objects.get(id=district)
                insert_into_district_staff(newForm.fname,newForm.lname,newForm.mobile,newForm.email,gender,district,dist.province_id,level.user_id)                                    
            dist_staff=Districtstaff.objects.latest('id')
            assign_access_level(user.id,dist_staff.id,3,"District User")
            messages.success(request, "District Staff Created successfully!")
            write_to_file(request.user,"District Staff Created successfully!",dist_staff.id)
            return redirect('/staff/districtstaff')
    context={"title":"Create District Staff","form":form,"level":level.level,"districts":districts}
    return render(request,'staff/creatediststaff.html',context)
    

@permission_required('staff.view_districtstaff')
def district_staff(request):
    level=Userlevel.objects.get(user=request.user)
    if user_validate(request,level.level,level.staff):
        if level.level==1:
            records=Districtstaff.objects.all().order_by('-id')
            totalrecords=Districtstaff.objects.all().count()
            filtered=records.count()
            myFilter=DistrictStaffFilter(request.POST,queryset=records)
        elif level.level==2:
            staff=Provincialstaff.objects.get(id=level.staff)
            records=Districtstaff.objects.filter(province_id=staff.province_id).order_by('-id')
            totalrecords=Districtstaff.objects.filter(province_id=staff.province_id).count()
            filtered=records.count()
            myFilter=DistrictStaffFilter2(request.POST,queryset=records)
        elif level.level==3:
            staff=Districtstaff.objects.get(id=level.staff)
            records=Districtstaff.objects.filter(district_id=staff.district_id).order_by('-id')
            totalrecords=Districtstaff.objects.filter(district_id=staff.district_id).count()
            filtered=records.count()
            myFilter=DistrictStaffFilter3(request.POST,queryset=records)
        elif level.level==4:
            staff=Staff.objects.get(id=level.staff)
            records=Districtstaff.objects.filter(district_id=staff.district_id).order_by('-id')
            totalrecords=Districtstaff.objects.filter(district_id=staff.district_id).count()
            filtered=records.count()
            myFilter=DistrictStaffFilter3(request.POST,queryset=records)
        else:
            records=DistrictStaffFilterNone.objects.none()
            totalrecords=0
            myFilter=StaffFilterNone(request.POST,queryset=records)
        records=myFilter.qs
        paginator=Paginator(records,20)
        page_num=request.GET.get('page', 1)
        records=paginator.get_page(page_num)
        pagecount=int(len(list(records)))
        counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
        context={"title":"District Staff","records":records,"districtstaff":"active","counted":counted,"myFilter":myFilter,}
        return render(request,'staff/districtstaff.html',context)
    return redirect('/')

@permission_required('staff.change_districtstaff')
def update_dist_staff(request,id=None):
    record = get_object_or_404(Districtstaff, id=id)
    form = UpdateDistrictStaffForm(request.POST or None, instance=record)
    if form.is_valid():
        newForm=form.save(commit=False)
        if nrc_validated(request,newForm.nrc):
            dist=District.objects.get(id=newForm.district_id)
            newForm.province_id=dist.province_id
            newForm.save()
            messages.success(request, "District Staff Updated successfully!")
            write_to_file(request.user,"District Staff Updated successfully!",record.id)
            search=record.mobile+" "+newForm.nrc+" "+newForm.empnumber+" "+newForm.lname+" "+newForm.fname+" "+record.email
            newForm.search=search
            record.author=request.user
            record.save()
            return redirect('/staff/districtstaff')
    context = {"title": 'Update District Staff',"record": record,"form": form,}
    return render(request,'staff/updatediststaff.html',context)


@permission_required('staff.add_provincialstaff')
def create_prov_staff(request):
    provinces=Province.objects.all()
    level=Userlevel.objects.get(user=request.user)
    form=RegisterStaff(request.POST or None)
    if form.is_valid():
        newForm=form.save(commit=False)
        if username_validated(request,newForm.userid) and phone_validated(request,newForm.mobile):
            insert_into_user(newForm.userid.lower(),newForm.fname,newForm.lname,newForm.email,False,newForm.mobile)
            newForm.userid.lower()
            newForm.save()
            user=User.objects.latest('id')
            gender=request.POST.get('gender')
            user_role = Group.objects.get(name="Provincial_User") 
            insert_into_userhistory(user.id,newForm.fname,newForm.lname,newForm.email,True,user.last_login,user.date_joined,user_role,request.user)
            user_role.user_set.add(user.id)
            if level.level==2:
                creator=Provincialstaff.objects.get(id=level.staff)
                insert_into_province_staff(newForm.fname,newForm.lname,newForm.mobile,newForm.email,gender,creator.province_id,level.user_id)                                    
            else:
                province=request.POST.get('province')
                insert_into_province_staff(newForm.fname,newForm.lname,newForm.mobile,newForm.email,gender,province,level.user_id)                                    
            prov_staff=Districtstaff.objects.latest('id')
            Provincialstaff.objects.filter(id=prov_staff.id).update(search=user.username+" "+prov_staff.fname+" "+prov_staff.lname+" "+prov_staff.mobile)
            assign_access_level(user.id,prov_staff.id,2,"Provincial User")
            messages.success(request, "Provincial Staff Created successfully!")
            write_to_file(request.user,"Provincial Staff Created successfully!",prov_staff.id)
            return redirect('/staff/provincialstaff')
    context={"title":"Create Provincial Staff","form":form,"level":level.level,"provinces":provinces}
    return render(request,'staff/createprovstaff.html',context)
    

@permission_required('staff.view_provincialstaff')
def provincial_staff(request):
    level=Userlevel.objects.get(user=request.user)
    if user_validate(request,level.level,level.staff):
        if level.level==1:
            records=Provincialstaff.objects.all().order_by('-id')
            totalrecords=Provincialstaff.objects.filter().count()
            filtered=records.count()
            myFilter=ProvincialStaffFilter(request.POST,queryset=records)
        elif level.level==2:
            staff=Provincialstaff.objects.get(id=level.staff)
            records=Provincialstaff.objects.filter(province_id=staff.province_id).order_by('-id')
            totalrecords=Provincialstaff.objects.filter(province_id=staff.province_id).count()
            filtered=records.count()
            myFilter=ProvincialStaffFilter2(request.POST,queryset=records)
        elif level.level==3:
            staff=Districtstaff.objects.get(id=level.staff)
            records=Provincialstaff.objects.filter(province_id=staff.province_id).order_by('-id')
            totalrecords=Provincialstaff.objects.filter(province_id=staff.province_id).count()
            filtered=records.count()
            myFilter=ProvincialStaffFilter3(request.POST,queryset=records)
        elif level.level==4:
            staff=Staff.objects.get(id=level.staff)
            records=Provincialstaff.objects.filter(province_id=staff.province_id).order_by('-id')
            totalrecords=Provincialstaff.objects.filter(province_id=staff.province_id).count()
            filtered=records.count()
            myFilter=ProvincialStaffFilter4(request.POST,queryset=records)
        else:
            records=Districtstaff.objects.none()
            totalrecords=0
            myFilter=StaffFilterNone(request.POST,queryset=records)
        records=myFilter.qs
        paginator=Paginator(records,20)
        page_num=request.GET.get('page', 1)
        records=paginator.get_page(page_num)
        pagecount=int(len(list(records)))
        counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
        context={"title":"Provincial Staff","records":records,"provincialstaff":"active","counted":counted,"myFilter":myFilter,}
        return render(request,'staff/provincialstaff.html',context)
    return redirect('/')


@permission_required('staff.change_provincialstaff')
def update_prov_staff(request,id=None):
    record = get_object_or_404(Provincialstaff, id=id)
    form = UpdateProvincialStaffForm(request.POST or None, instance=record)
    if form.is_valid():
        newForm=form.save(commit=False)
        if nrc_validated(request,newForm.nrc):
            search=record.mobile+" "+newForm.nrc+" "+newForm.empnumber+" "+newForm.lname+" "+newForm.fname+" "+record.email
            newForm.search=search
            newForm.save()
            messages.success(request, "Provincial Staff Updated successfully!")
            write_to_file(request.user,"Provincial Staff Updated successfully!",record.id)
            record.author=request.user
            record.save()
            return redirect('/staff/provincialstaff')
    context = {"title": 'Update Provincial Staff',"record": record,"form": form,}
    return render(request,'staff/updateprovstaff.html',context)


@permission_required('staff.view_myprofile')
def my_profile(request):
    level=Userlevel.objects.get(user=request.user)
    if level.level==1:
        messages.warning(request, "No PROFILE")
        return redirect('/')
    elif level.level==2:      
        profile=Provincialstaff.objects.get(id=level.staff)
        context={"title":"My Profile","profile":profile,"myprofile":"active","showform":"none","level":level.level}
        return render(request,'staff/myprofile.html',context)
    elif level.level==3:      
        profile=Districtstaff.objects.get(id=level.staff)
        context={"title":"My Profile","profile":profile,"myprofile":"active","showform":"none","level":level.level}
        return render(request,'staff/myprofile.html',context)
    elif level.level==4:      
        profile=Staff.objects.get(id=level.staff)
        if profile.status=="Disapproved":
            messages.warning(request, "Your Information is Disapproved: "+str(profile.comment))
        context={"title":"My Profile","profile":profile,"myprofile":"active","showform":"none","level":level.level}
        return render(request,'staff/myprofile.html',context)
    else:
        messages.error(request, "Invalid User!!!")
        return redirect('/')
    
        

@permission_required('staff.change_myprofile')
def update_mybio_profile(request):
    level=Userlevel.objects.get(user=request.user)
    if level.level==4:
        record = get_object_or_404(Staff, id=level.staff)
        form = UpdateStaffBioForm(request.POST or None, instance=record)
        if record.is_updated:
            form.fields['district'].widget = forms.HiddenInput()
            form.fields['mobile'].widget = forms.HiddenInput()
        if form.is_valid():
            newForm=form.save(commit=False)
            if phone_validated(request,newForm.mobile):
                dist=District.objects.get(id=newForm.district_id)
                newForm.province_id=dist.province_id
                if record.empnumber == None:
                     search=record.mobile+" "+newForm.lname+" "+newForm.fname+" "+record.email
                else:
                    search=record.mobile+" "+record.nrc+" "+record.empnumber+" "+record.tsnumber+" "+newForm.lname+" "+newForm.fname+" "+record.email
                newForm.search=search
                newForm.save()
                messages.success(request, "Profile Updated successfully!")
                write_to_file(request.user,"Bio Profile Updated successfully!",record.id)
                return redirect('/staff/updatemyworkprofile')
        context = {"title": 'Update My Profile',"record": record,"form": form,"showform":"none","updatemybioprofile":"active",}
        return render(request,'staff/updatemyprofile.html',context)
    elif level.level==3:
        record = get_object_or_404(Districtstaff, id=level.staff)
        form = UpdateDistrictStaffForm(request.POST or None, instance=record)
        form.fields['district'].widget = forms.HiddenInput()
        if record.is_updated:
            form.fields['mobile'].widget = forms.HiddenInput()
        if form.is_valid():
            newForm=form.save(commit=False)
            if phone_validated(request,newForm.mobile) and nrc_validated(request,newForm.nrc):
                newForm.status="Updated"
                newForm.is_updated=True
                search=record.mobile+" "+newForm.nrc+" "+newForm.empnumber+" "+newForm.lname+" "+newForm.fname+" "+record.email
                newForm.search=search
                newForm.save()
                messages.success(request, "Profile Updated successfully!")
                write_to_file(request.user,"Bio Profile Updated successfully!",record.id)
                return redirect('/staff/myprofile')
        context = {"title": 'Update My Profile',"record": record,"form": form,"showform":"none",}
        return render(request,'staff/updatediststaff.html',context)
    else:
        record = get_object_or_404(Provincialstaff, id=level.staff)
        form = UpdateProvincialStaffForm(request.POST or None, instance=record)
        form.fields['province'].widget = forms.HiddenInput()
        if record.is_updated:
            form.fields['mobile'].widget = forms.HiddenInput()
        if form.is_valid():
            newForm=form.save(commit=False)
            if phone_validated(request,newForm.mobile) and nrc_validated(request,newForm.nrc):
                dist=District.objects.get(id=newForm.district_id)
                newForm.province_id=dist.province_id
                newForm.status="Updated"
                newForm.is_updated=True
                search=record.mobile+" "+newForm.nrc+" "+newForm.empnumber+" "+newForm.lname+" "+newForm.fname+" "+record.email
                newForm.search=search
                newForm.save()
                messages.success(request, "Profile Updated successfully!")
                write_to_file(request.user,"Bio Profile Updated successfully!",record.id)
                return redirect('/staff/myprofile')
        context = {"title": 'Update My Profile',"record": record,"form": form,"showform":"none",}
        return render(request,'staff/updateprovstaff.html',context)


@permission_required('staff.change_myprofile')
def update_mywork_profile(request):
    level=Userlevel.objects.get(user=request.user)
    record = get_object_or_404(Staff, id=level.staff)
    schools=School.objects.filter(district=record.district)
    form = UpdateStaffWorkForm(request.POST or None, instance=record)
    if form.is_valid():
        newForm=form.save(commit=False)
        if nrc_validated(request,newForm.nrc):
            newForm.school_id=request.POST.get('school')
            newForm.is_updated=True
            newForm.status="Updated"
            newForm.save()
            search=record.mobile+" "+newForm.nrc+""+newForm.tsnumber+" "+newForm.empnumber+" "+record.lname+" "+record.fname+" "+record.email
            record.search=search
            record.save()
            messages.success(request, "Work Profile Updated successfully!")
            write_to_file(request.user,"Work Profile Updated successfully!",record.id)
            return redirect('/staff/myprofile')
    context = {"title": 'Update Profile',"record": record,"form": form,"showform":"none","updatemyworkprofile":"active","schools":schools,"schl":record.school}
    return render(request,'staff/updatemyworkprofile.html',context)


@permission_required('staff.change_myprofile')
def update_myphoto(request):
    level=Userlevel.objects.get(user=request.user)
    if level.level==4:
        record = get_object_or_404(Staff, id=level.staff)
        form = UploadStaffPhoto(request.POST or None,request.FILES or None, instance=record)
    elif level.level==3:
        record = get_object_or_404(Districtstaff, id=level.staff)
        form = UploadDistrictStaffPhoto(request.POST or None,request.FILES or None, instance=record)
    else:
        record = get_object_or_404(Provincialstaff, id=level.staff)
        form = UploadProvincialStaffPhoto(request.POST or None,request.FILES or None, instance=record)
    if form.is_valid():
        form.save()
        messages.success(request, "Profile Photo Updated successfully!")
        write_to_file(request.user,"Profile Photo Updated successfully!",record.id)
        return redirect('/staff/myprofile')
    context = {"title": 'Update My Profile Photo',"record": record,"form": form,"level":level.level}
    return render(request,'staff/uploadstaffphoto.html',context)


@permission_required('staff.change_myprofile')
def submit_myinfo(request):
    level=Userlevel.objects.get(user=request.user)
    record = get_object_or_404(Staff, id=level.staff)
    maindocs=Maindocument.objects.filter(is_active=True).count()
    mydocs=Staffdocument.objects.filter(staff_id=level.staff,is_uploaded=True).count()
    myuploads=Qualification.objects.filter(staff_id=level.staff,is_uploaded=False).count()
    if myuploads > 0:
        messages.error(request, "Please Upload All your Qualification documents to proceed!")
        write_to_file(request.user,"Please Upload All your Qualification documents to proceed!",record.id)
    else:
        if maindocs==mydocs:
            record.status="Pending"
            record.save()
            messages.success(request, "Information Submitted successfully!")
            write_to_file(request.user,"Information Submitted successfully!",record.id)
        else:
            messages.error(request, "Please Upload All Main documents to proceed!")
            write_to_file(request.user,"Please Upload All Main documents to proceed!",record.id)
    return redirect('/staff/myprofile')



@permission_required('staff.change_myprofile')
def cancel_mysubmission(request):
    level=Userlevel.objects.get(user=request.user)
    record = get_object_or_404(Staff, id=level.staff)
    record.status="Updated"
    record.save()
    work_on_documents(record.id,"Uploaded")
    messages.success(request, "Submission Cancelled successfully!")
    write_to_file(request.user,"Submission Cancelled successfully!",record.id)
    return redirect('/staff/myprofile')


@permission_required('staff.change_myprofile')
def initialize_myprofile(request):
    level=Userlevel.objects.get(user=request.user)
    record = get_object_or_404(Staff, id=level.staff)
    record.school=None
    record.district=None
    record.province=None
    record.status="Registered"
    record.is_updated=False
    record.save()
    staffnumber=Staff.objects.filter(school_id=record.school_id).count()
    School.objects.filter(id=record.school_id).update(staffnumber=staffnumber)
    staffnumber=Staff.objects.filter(district_id=record.district_id).count()
    District.objects.filter(id=record.district_id).update(staffnumber=staffnumber)
    staffnumber=Staff.objects.filter(province_id=record.province_id).count()
    Province.objects.filter(id=record.province_id).update(staffnumber=staffnumber)
    work_on_documents(record.id,"Uploaded")
    messages.success(request, "Profile Initialized successfully!")
    write_to_file(request.user,"Profile Initialized successfully!",record.id)
    return redirect('/staff/myprofile')



def nrc_validated(request,nrc):
    if len(nrc)==11:
        mformat1=nrc[6]
        mformat2=nrc[9]
        if mformat1=="/" and mformat2=="/":
            range1=nrc[0:6]
            range2=nrc[7:9]
            range3=nrc[10]
            if range1.isdigit() and range2.isdigit() and range3.isdigit():
                if (range3=="1" or range3=="2") and (int(range2)>9):
                    #messages.success(request, "Coooool"+str(range1)+""+mformat1+""+str(range2)+""+mformat2+""+str(range3))
                    return True
                else:
                    messages.error(request, "Invalid NRC range [" +str(range2)+"/"+str(range3)+"]")
                    return False
            else:
                messages.error(request, "Invalid Charater used in NRC [" +str(nrc)+"]")
                return False
        else:
            messages.error(request, "Invalid NRC format [" +str(nrc)+"]")
            return False
    else:
        messages.error(request, "NRC should be composed of 11 digits") 
        return False
    
    
def work_on_documents(staff,status):
    Documentupload.objects.filter(staff_id=staff).update(status=status)
    Staffdocument.objects.filter(staff_id=staff).update(status=status)

def insert_into_district_staff(fname,lname,mobile,email,gender,district,province,author):
    dist_staff=Districtstaff()
    dist_staff.fname=fname.strip()
    dist_staff.lname=lname.strip()
    dist_staff.mobile=mobile
    dist_staff.email=email.lower().strip()
    dist_staff.gender=gender
    dist_staff.district_id=district
    dist_staff.province_id=province
    dist_staff.author_id=author
    dist_staff.save()
    
def insert_into_province_staff(fname,lname,mobile,email,gender,province,author):
    prov_staff=Provincialstaff()
    prov_staff.fname=fname.strip()
    prov_staff.lname=lname.strip()
    prov_staff.mobile=mobile
    prov_staff.email=email.lower().strip()
    prov_staff.gender=gender
    prov_staff.province_id=province
    prov_staff.author_id=author
    prov_staff.save()