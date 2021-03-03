from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from .filters import *
import datetime
from django.utils import six
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from staff.models import Userlevel,Staff,Districtstaff,Provincialstaff
from django.forms import modelformset_factory
import csv
from django.http import HttpResponse


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

@permission_required('school.view_schoolmodule')		
def school_module(request):
	context={"title":"Schools","showform":"none",}
	return render(request,'module.html',context)


@permission_required('school.add_province')
def create_province(request):
    form=ProvinceForm(request.POST or None)
    if form.is_valid():
        newForm=form.save(commit=False)
        newForm.author=request.user
        newForm.save()
        messages.success(request, "Province Created successfully!")
        province=Province.objects.latest('id')
        write_to_file(request.user,"Province Created successfully!",province.id)
        return redirect('/school/allprovinces')
    context={"title":"Create Province","form":form,}
    return render(request,'school/create.html',context)


@permission_required('school.view_province')
def all_provinces(request):
	records=Province.objects.all().order_by('-id')
	totalrecords=Province.objects.filter().count()
	filtered=records.count()
	paginator=Paginator(records,10)
	page_num=request.GET.get('page', 1)
	records=paginator.get_page(page_num)
	pagecount=int(len(list(records)))
	counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
	context={"title":"Provinces","records":records,"allprovinces":"active","counted":counted,"showform":"none",}
	return render(request,'school/allprovinces.html',context)


@permission_required('school.change_province')
def update_province(request,id=None):
    record = get_object_or_404(Province, id=id)
    form = ProvinceForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        messages.success(request, "Province Updated successfully!")
        write_to_file(request.user,"Province Updated successfully!",record.id)
        return redirect('/school/allprovinces')
    context = {"title": 'Update Province',"record": record,"form": form,}
    return render(request,'school/createprovince.html',context)



@permission_required('boundary.add_district')
def create_district(request,id):
    record = get_object_or_404(Province, id=id)
    DistrictFormSet=modelformset_factory(District,fields=('district',),extra=10)
    form=DistrictFormSet(request.POST or None)
    if form.is_valid():
        newForm=form.save(commit=False)
        count=0
        for new in newForm:
            new.province_id=record.id
            new.author=request.user
            new.save()
            count+=1
            district=District.objects.latest('id')
            write_to_file(request.user, "District Created successfully!",district.id)
            districts=District.objects.filter(province_id=record.id).count()
            record.districtnumber=districts
            record.save()
        messages.success(request, str(count)+" District(s) Created successfully!")
        return redirect('/school/allprovinces')
    form=DistrictFormSet(queryset=District.objects.none())
    context={"title":"Create District(s) in "+str(record.province),"form":form,}
    return render(request,'school/create.html',context)


@permission_required('school.view_district')
def all_districts(request):
	records=District.objects.all().order_by('-id')
	totalrecords=District.objects.filter().count()
	filtered=records.count()
	myFilter=DistrictFilter(request.POST,queryset=records)
	records=myFilter.qs
	paginator=Paginator(records,20)
	page_num=request.GET.get('page', 1)
	records=paginator.get_page(page_num)
	pagecount=int(len(list(records)))
	counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
	context={"title":"Districts","records":records,"alldistricts":"active","counted":counted,"myFilter":myFilter,}
	return render(request,'school/alldistricts.html',context)


@permission_required('school.change_district')
def update_district(request,id=None):
    record = get_object_or_404(District, id=id)
    form = DistrictForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        messages.success(request, "District Updated successfully!")
        write_to_file(request.user,"District Updated successfully!",record.id)
        return redirect('/school/alldistricts')
    context = {"title": 'Update District',"record": record,"form": form,}
    return render(request,'school/create.html',context)


@permission_required('school.add_school')
def create_school(request):
    form=SchoolForm(request.POST or None)
    if form.is_valid():
        newForm=form.save(commit=False)
        dist=District.objects.get(id=newForm.district_id)
        newForm.province_id=dist.province_id
        newForm.author=request.user
        newForm.save()
        school=School.objects.latest('id')
        schools=School.objects.filter(district_id=school.district_id).count()
        District.objects.filter(id=school.district_id).update(schoolnumber=schools)
        schools=School.objects.filter(province_id=school.province_id).count()
        Province.objects.filter(id=school.province_id).update(schoolnumber=schools)
        messages.success(request, "School Created successfully!")
        write_to_file(request.user,"School Created successfully!",school.id)
        return redirect('/school/allschools')
    context={"title":"Create School","form":form,}
    return render(request,'school/create.html',context)


@permission_required('school.view_school')
def all_schools(request):
	level=Userlevel.objects.get(user=request.user)
	if level.level==1:
		records=School.objects.all().order_by('-id')
		totalrecords=School.objects.all().count()
		filtered=records.count()
		myFilter=SchoolFilter(request.POST,queryset=records)
		schoolid=0
		boundary=""
	elif level.level==2:
		staff=Provincialstaff.objects.get(id=level.staff)
		if staff.is_updated:
			records=School.objects.filter(province_id=staff.province_id).order_by('-id')
			totalrecords=Staff.objects.filter(province_id=staff.province_id).count()
			filtered=records.count()
			myFilter=SchoolFilter2(request.POST,queryset=records)
			schoolid=0
			boundary=""
		else:
			messages.success(request, "School Updated successfully!")
	elif level.level==3:
		staff=Districtstaff.objects.get(id=level.staff)
		if staff.is_updated:
			records=School.objects.filter(district_id=staff.district_id).order_by('-id')
			totalrecords=Staff.objects.filter(district_id=staff.district_id).count()
			filtered=records.count()
			schoolid=0
			myFilter=SchoolFilter3(request.POST,queryset=records)
			boundary="in "+str(staff.province)
		else:
			messages.warning(request, "Please update your profile to proceed!")
			return redirect('/')
	elif level.level==4:
		staff=Staff.objects.get(id=level.staff)
		if staff.is_updated:
			records=School.objects.filter(district_id=staff.district_id).order_by('-id')
			totalrecords=Staff.objects.filter(district_id=staff.district_id).count()
			filtered=records.count()
			schoolrecord=School.objects.get(id=staff.school_id)
			schoolid=schoolrecord.id
			myFilter=SchoolFilter3(request.POST,queryset=records)
			boundary="in "+str(staff.district)
		else:
			messages.warning(request, "Please update your profile to proceed!")
			return redirect('/')
	else:
		records=School.objects.none()
		totalrecords=0
		myFilter=SchoolFilterNone(request.POST,queryset=records)
	records=myFilter.qs
	filteredrecords=records
	paginator=Paginator(records,20)
	page_num=request.GET.get('page', 1)
	records=paginator.get_page(page_num)
	pagecount=int(len(list(records)))
	counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
	form=ExportSchool(request.POST or None)
	if form['export_to_file'].value() == True:
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=StaffList.csv'
		writer = csv.writer(response)
		writer.writerow(['TS No.','FIRST NAME','LAST NAME','OTHER NAMES','GENDER','TITLE','NRC','CONTACT No.','EMAIL','DOB','FIRST APPOINTMENT','POSITION',
			'ORGANIZATION', 'DISTRICT','PROVINCE','ADDRESS','STATUS','APPLICANT No.','ACTIVE','CYCLE','CREATEDBY','DATECREATED','REMARKS'])
		if pagecount>0:
			for row in filteredrecords:
				write_to_file(str(request.user)+"_downloads",str(request.user)+" Exported "+str(filteredrecords.count())+" Station Staff Record(s)",row.id)
				writer.writerow([row.tsnumber,row.fname,row.lname,row.mname,row.gender,row.title,row.nrc,row.mobile,row.email,row.birth_date,row.first_appointment,row.position,
                     row.school,row.isconfirmed,row.empnumber,row.status,row.district,row.province,row.qualifications,row.comment,row.is_updated,row.is_active,row.datecreated,row.author])
			return response
		else:
			messages.error(request, "No Records to Export!")
	context={"title":"All Schools "+str(boundary),"records":records,"schoolid":schoolid,"allschools":"active","counted":counted,"myFilter":myFilter,"form1":form}
	return render(request,'school/allschools.html',context)


@permission_required('school.change_school')
def update_school(request,id=None):
	record = get_object_or_404(School, id=id)
	form = SchoolForm(request.POST or None, instance=record)
	form.fields['district'].widget = forms.HiddenInput()
	if form.is_valid():
		newForm=form.save(commit=False)	
		district=District.objects.get(id=newForm.district_id)
		province=Province.objects.get(id=district.province_id)
		newForm.province_id=province.id
		newForm.author=request.user
		newForm.save()	
		messages.success(request, "School Updated successfully!")
		write_to_file(request.user,"School Updated successfully!",record.id)

		schools=School.objects.filter(district_id=newForm.district_id).count()
		District.objects.filter(id=newForm.district_id).update(schoolnumber=schools)
		schools=School.objects.filter(province_id=province.id).count()
		Province.objects.filter(id=province.id).update(schoolnumber=schools)

		districtid=request.POST.get("districtid")
		provinceid=request.POST.get("provinceid")
		
		if int(districtid) == int(newForm.district_id):
			pass
		else:
			schools=School.objects.filter(district_id=districtid).count()
			District.objects.filter(id=districtid).update(schoolnumber=schools)
			schools=School.objects.filter(province_id=provinceid).count()
			Province.objects.filter(id=provinceid).update(schoolnumber=schools)
			Staff.objects.filter(district_id=districtid).update(district_id=newForm.district_id,province_id=province.id)
	
		return redirect('/school/allschools')
	context = {"title": 'Update School',"record": record,"form": form,}
	return render(request,'school/updateschool.html',context)






