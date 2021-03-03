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
from staff.models import Userlevel

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


@permission_required('qualification.view_qualificationmodule')		
def qualication_module(request):
	context={"title":"Qualifications","showform":"none",}
	return render(request,'module.html',context)


@permission_required('qualification.view_qualification')
def all_qualifications(request):
    records=Qualification.objects.all().order_by('-id')
    totalrecords=Qualification.objects.filter().count()
    filtered=records.count()
    myFilter=QualificationFilter(request.POST,queryset=records)
    records=myFilter.qs
    paginator=Paginator(records,20)
    page_num=request.GET.get('page', 1)
    records=paginator.get_page(page_num)
    pagecount=int(len(list(records)))
    counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
    context={"title":"All Qaulifications","records":records,"allqualifications":"active","counted":counted,"myFilter":myFilter,}
    return render(request,'qualification/allqualifications.html',context)


@permission_required('qualification.add_maindocument')
def create_maindocument(request):
    form=MaindocumentForm(request.POST or None)
    if form.is_valid():
        newForm=form.save(commit=False)
        newForm.author=request.user
        newForm.save()
        messages.success(request, "Main Document Created successfully!")
        document=Maindocument.objects.latest('id')
        write_to_file(request.user,"Main Document Created successfully!",document.id)
        return redirect('/document/allmaindocuments')
    context={"title":"Create Main Document","form":form,}
    return render(request,'document/createmaindocument.html',context)


@permission_required('qualification.view_maindocument')
def all_maindocuments(request):
    records=Maindocument.objects.all().order_by('-id')
    totalrecords=Maindocument.objects.filter().count()
    filtered=records.count()
    myFilter=MaindocumentFilter(request.POST,queryset=records)
    records=myFilter.qs
    pagecount=int(len(list(records)))
    counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
    context={"title":"Main documents","records":records,"allmaindocuments":"active","counted":counted,"myFilter":myFilter,}
    return render(request,'document/allmaindocuments.html',context)


@permission_required('qualification.change_maindocument')
def update_maindocument(request,id=None):
    record = get_object_or_404(Maindocument, id=id)
    form = MaindocumentForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        record.author=request.user
        record.save()
        messages.success(request, "Main Document Updated successfully!")
        write_to_file(request.user,"Main Document Updated successfully!",record.id)
        return redirect('/document/allmaindocuments')
    context = {"title": 'Update Main Document',"record": record,"form": form,}
    return render(request,'document/createmaindocument.html',context)


@permission_required('qualification.add_category')
def create_category(request):
    form=CategoryForm(request.POST or None)
    if form.is_valid():
        newForm=form.save(commit=False)
        newForm.author=request.user
        newForm.save()
        messages.success(request, "Category Created successfully!")
        category=Category.objects.latest('id')
        write_to_file(request.user,"Category Created successfully!",category.id)
        return redirect('/qualification/allcategories')
    context={"title":"Create Category","form":form,}
    return render(request,'category/createcategory.html',context)


@permission_required('qualification.view_category')
def all_categories(request):
    records=Category.objects.all().order_by('-id')
    totalrecords=Category.objects.filter().count()
    filtered=records.count()
    myFilter=CategoryFilter(request.POST,queryset=records)
    records=myFilter.qs
    pagecount=int(len(list(records)))
    counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
    context={"title":"Field Categories","records":records,"allcategories":"active","counted":counted,"myFilter":myFilter,}
    return render(request,'category/allcategories.html',context)


@permission_required('qualification.change_category')
def update_category(request,id=None):
    record = get_object_or_404(Category, id=id)
    form = CategoryForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        record.author=request.user
        record.save()
        messages.success(request, "Category Updated successfully!")
        write_to_file(request.user,"Category Updated successfully!",record.id)
        return redirect('/qualification/allcategories')
    context = {"title": 'Update Category',"record": record,"form": form,}
    return render(request,'category/createcategory.html',context)


@permission_required('qualification.add_categorylevel')
def create_categorylevel(request):
    form=CategoryLevelForm(request.POST or None)
    if form.is_valid():
        newForm=form.save(commit=False)
        newForm.author=request.user
        newForm.save()
        messages.success(request, "Category Level Created successfully!")
        categorylevel=Categorylevel.objects.latest('id')
        write_to_file(request.user,"Category Level Created successfully!",categorylevel.id)
        return redirect('/qualification/categorylevels')
    context={"title":"Create Category","form":form,}
    return render(request,'category/createcategorylevel.html',context)


def category_levels(request):
    records=Categorylevel.objects.all().order_by('-id')
    totalrecords=Categorylevel.objects.filter().count()
    filtered=records.count()
    myFilter=CategorylevelFilter(request.POST,queryset=records)
    records=myFilter.qs
    pagecount=int(len(list(records)))
    counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
    context={"title":"Qualification Levels","records":records,"categorylevels":"active","counted":counted,"myFilter":myFilter,}
    return render(request,'category/categorylevels.html',context)


@permission_required('qualification.add_qualification')
def add_qualification(request,id):
    record = get_object_or_404(Staff,id=id)
    form=QualificationForm(request.POST or None)
    if form.is_valid():
        newForm=form.save(commit=False)
        newForm.staff_id=record.id
        newForm.author=request.user
        newForm.save()
        messages.success(request, "Staff Qualification added successfully!")
        qualifications=Qualification.objects.filter(staff_id=record.id).count()
        Staff.objects.filter(id=record.id).update(qualifications=qualifications)
        qualification=Qualification.objects.latest('id')
        qualification.key = ''.join(format(i, 'b') for i in bytearray(str(qualification.id), encoding ='utf-8')) 
        qualification.save()
        write_to_file(request.user,"Qualification added successfully!",qualification.id)
        return redirect('/qualification/staffqualifications/'+str(record.empnumber)+'/'+str(record.id))
    context={"title":"Add Qualification for "+str(record.fname)+" "+str(record.lname),"staff":record,"form":form,}
    return render(request,'qualification/addqualification.html',context)


@permission_required('qualification.view_qualification')
def staff_qualifications(request,id):
    record = get_object_or_404(Staff, id=id)
    records=Qualification.objects.filter(staff_id=record.id).order_by('-id')
    totalrecords=Qualification.objects.filter(staff_id=record.id).count()
    filtered=records.count()
    myFilter=QualificationFilter(request.POST,queryset=records)
    records=myFilter.qs
    paginator=Paginator(records,20)
    page_num=request.GET.get('page', 1)
    records=paginator.get_page(page_num)
    pagecount=int(len(list(records)))
    counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
    context={"title": "Qualifications", "sub":str(record.fname)+" "+str(record.lname)+"'s","records":records,"staff":record,"counted":counted,"myFilter":myFilter,}
    return render(request,'qualification/staffqualifications.html',context)


@permission_required('qualification.add_myqualification')
def add_myqualification(request):
    form=QualificationForm(request.POST or None)
    if form.is_valid():
        level=Userlevel.objects.get(user=request.user)
        newForm=form.save(commit=False)
        newForm.staff_id=level.staff
        newForm.author=request.user
        newForm.save()
        messages.success(request, "Qualification added successfully!")
        qualifications=Qualification.objects.filter(staff_id=level.staff).count()
        Staff.objects.filter(id=level.staff).update(qualifications=qualifications)
        qualification=Qualification.objects.latest('id')
        qualification.key = ''.join(format(i, 'b') for i in bytearray(str(qualification.id), encoding ='utf-8')) 
        qualification.save()
        write_to_file(request.user,"Qualification added successfully!",qualification.id)
        return redirect('/qualification/myqualifications')
    context={"title":"Add Qualification","form":form,}
    return render(request,'qualification/addqualification.html',context)


@permission_required('qualification.view_myqualification')
def my_qualification(request):
    level=Userlevel.objects.get(user=request.user)
    myrecord=Staff.objects.get(id=level.staff)
    records=Qualification.objects.filter(staff_id=level.staff).order_by('-id')
    totalrecords=Qualification.objects.filter(staff_id=level.staff).count()
    filtered=records.count()
    myFilter=QualificationFilter(request.POST,queryset=records)
    records=myFilter.qs
    paginator=Paginator(records,20)
    page_num=request.GET.get('page', 1)
    records=paginator.get_page(page_num)
    pagecount=int(len(list(records)))
    counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
    context={"title":"My Qaulifications","records":records,"myqualifications":"active","counted":counted,"myFilter":myFilter,"myrecord":myrecord}
    return render(request,'qualification/myqualifications.html',context)


@permission_required('qualification.change_myqualification')
def update_myqualification(request,id=None):
    level=Userlevel.objects.get(user=request.user)
    record = get_object_or_404(Qualification, id=id, staff_id=level.staff)
    form = QualificationForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        messages.success(request, "Qualification Updated successfully!")
        write_to_file(request.user,"Qualification Updated successfully!",record.id)
        return redirect('/qualification/myqualifications')
    context = {"title": 'Update Qualification',"record": record,"form": form,}
    return render(request,'qualification/updatemyqualification.html',context)


@permission_required('qualification.delete_myqualification')
def delete_myqualification(request,id):
    level=Userlevel.objects.get(user=request.user)
    record = get_object_or_404(Qualification, id=id)
    write_to_file(request.user,"Qualification deleted Successfully!",record.id)
    record.delete()
    qualifications=Qualification.objects.filter(staff_id=level.staff).count()
    Staff.objects.filter(id=level.staff).update(qualifications=qualifications)
    messages.success(request, "Qualification Record deleted successfully!")
    return redirect('/qualification/myqualifications')


@permission_required('qualification.add_mydocument')
def upload_mydocument(request,id):
    level=Userlevel.objects.get(user=request.user)
    record = get_object_or_404(Qualification, id=id)
    form = UploadDocumentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        newForm=form.save(commit=False)
        newForm.author=request.user
        newForm.qualification_id=record.id
        newForm.staff_id=level.staff
        newForm.save()
        documents=Documentupload.objects.filter(qualification_id=record.id).count()
        Qualification.objects.filter(id=record.id,staff_id=level.staff).update(documents=documents,is_uploaded=True)
        messages.success(request, "Document Uploaded successfully!")
        upload=Documentupload.objects.latest('id')
        upload.key = record.key
        upload.docname=str(upload.qualification)+"_"+upload.documentupload.name
        if upload.docname.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            pass
        else:
            upload.isimage=False
        upload.save()
        write_to_file(request.user,"Document Uploaded Successfully!",upload.id)
        return redirect('/qualification/myqualifications')
    context = {"title": 'Upload '+str(record.field)+' Document',"record": record,"form": form,}
    return render(request,'document/uploadmydocument.html',context)


@permission_required('qualification.view_mydocument')
def my_documents(request):
    level=Userlevel.objects.get(user=request.user)
    myrecord=Staff.objects.get(id=level.staff)
    records=Documentupload.objects.filter(staff_id=level.staff).order_by('-isimage')
    totalrecords=Documentupload.objects.filter(staff_id=level.staff).count()
    filtered=records.count()
    for record in records:
        pass
    paginator=Paginator(records,20)
    page_num=request.GET.get('page', 1)
    records=paginator.get_page(page_num)
    count=int(len(list(records)))
    mainrecords=Maindocument.objects.filter(is_active=True).order_by('-id')
    myuploads=Staffdocument.objects.filter(staff_id=level.staff)
    mainrecords_count=Staffdocument.objects.filter(staff_id=level.staff).count()
    pagecount=mainrecords_count+count
    totalrecords=totalrecords+mainrecords_count
    counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
    context={"title":"My Documents","mydocuments":"active","records":records,"showform":"none","counted":counted,"mainrecords":mainrecords,"myuploads":myuploads,"maincount":mainrecords_count,"count":count,"myrecord":myrecord}
    return render(request,'document/mydocuments.html',context)


@permission_required('qualification.view_mydocument')
def my_uploads(request,id):
    level=Userlevel.objects.get(user=request.user)
    record = get_object_or_404(Qualification, id=id)
    myrecord=Staff.objects.get(id=level.staff)
    records=Documentupload.objects.filter(staff_id=level.staff,qualification_id=record.id).order_by('-id')
    totalrecords=Documentupload.objects.filter(staff_id=level.staff,qualification_id=record.id).count()
    filtered=records.count()
    paginator=Paginator(records,20)
    page_num=request.GET.get('page', 1)
    records=paginator.get_page(page_num)
    pagecount=int(len(list(records)))
    counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
    context={"title":str(record.field)+" Document(s)","records":records,"showform":"none","counted":counted,"myrecord":myrecord}
    return render(request,'document/myuploads.html',context)


@permission_required('qualification.view_documentupload')
def staff_uploads353535(request,id,key):
    record = get_object_or_404(Qualification, id=id,key=key)
    staff=Staff.objects.get(id=record.staff_id)
    records=Documentupload.objects.filter(key=record.key,qualification_id=record.id).order_by('-id')
    totalrecords=Documentupload.objects.filter(key=key,qualification_id=record.id).count()
    filtered=records.count()
    paginator=Paginator(records,20)
    page_num=request.GET.get('page', 1)
    records=paginator.get_page(page_num)
    pagecount=int(len(list(records)))
    counted=str(pagecount) +" out of "+str(totalrecords)+" record(s)"
    empnumber=staff.empnumber
    staffid=record.staff_id
    name=staff.fname+" "+staff.lname
    context={"title":str(name)+"'s "+str(record.field)+" Document(s)","records":records,"empnumber":empnumber,"staffid":staffid,"showform":"none","counted":counted,}
    return render(request,'document/staffuploads.html',context)


@permission_required('qualification.change_mydocument')
def update_mydocument(request,id=None):
    level=Userlevel.objects.get(user=request.user)
    record = get_object_or_404(Documentupload, id=id)
    form = UploadDocumentForm(request.POST or None,request.FILES or None, instance=record)
    if form.is_valid():
        form.save()
        record.docname=str(record.qualification)+"_"+record.documentupload.name
        if record.docname.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            record.isimage=True
        else:
            record.isimage=False
        record.save()
        messages.success(request, "Document Updated successfully!")
        write_to_file(request.user,"Document Updated successfully!",record.id)
        return redirect('/document/myuploads/'+str(record.qualification_id))
    context = {"title": 'Update Document',"record": record,"form": form,}
    return render(request,'document/uploadmydocument.html',context)


@permission_required('qualification.delete_mydocument')
def delete_myupload(request,id):
    record = get_object_or_404(Documentupload, id=id)
    write_to_file(request.user,"Upload deleted Successfully!",record.id)
    record.delete()
    documents=Documentupload.objects.filter(qualification_id=record.qualification_id).count()
    if documents == 0:
        Qualification.objects.filter(id=record.qualification_id).update(documents=documents,is_uploaded=False)	
    else:
        Qualification.objects.filter(id=record.qualification_id).update(documents=documents,is_uploaded=True)	
    messages.success(request, "Upload deleted successfully!")
    return redirect('/document/myuploads/'+str(record.qualification_id))


@permission_required('qualification.add_mydocument')
def upload_maindocument(request,id):
    level=Userlevel.objects.get(user=request.user)
    record = get_object_or_404(Maindocument, id=id)
    form = UploadMainDocumentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        newForm=form.save(commit=False)
        newForm.author=request.user
        newForm.staff_id=level.staff
        newForm.document_id=record.id
        newForm.save()
        upload=Staffdocument.objects.latest('id')
        upload.docname=str(upload.document)+"_"+upload.documentupload.name
        if upload.docname.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            pass
        else:
            upload.isimage=False
        upload.save()
        
        documents=Staffdocument.objects.filter(document_id=record.id).count()
        Maindocument.objects.filter(id=record.id).update(documents=documents)
    
        Staffdocument.objects.filter(document_id=record.id,staff_id=level.staff).update(is_uploaded=False)
        Staffdocument.objects.filter(id=upload.id).update(is_uploaded=True)
       
        messages.success(request, "Main Document Uploaded successfully!") 
        write_to_file(request.user,"Main Document Uploaded Successfully!",upload.id)
        return redirect('/document/mydocuments')
    context = {"title": 'Upload '+str(record.docttype)+' Document',"record": record,"form": form,}
    return render(request,'document/uploadmaindocument.html',context)


@permission_required('qualification.delete_mydocument')
def delete_mymainupload(request,id):
	record = get_object_or_404(Staffdocument, id=id)
	write_to_file(request.user,"Upload deleted Successfully!",record.id)
	record.delete()
	documents=Staffdocument.objects.filter(document_id=record.document_id).count()
	Maindocument.objects.filter(id=record.document_id).update(documents=documents)	
	messages.success(request, "Upload deleted successfully!")
	return redirect('/document/mydocuments')


@permission_required('qualification.delete_category')
def delete_qualification(request,id):
    record = get_object_or_404(Category, id=id)
    write_to_file(request.user,"Category deleted Successfully!",record.id)
    categories=Qualification.objects.filter(category_id=record.id).count()
    if categories == 0:
        record.delete()
        messages.success(request, "Category deleted successfully!")
    else:
        messages.error(request, "This Category cannot be deleted now!")
    return redirect('/qualification/allcategories')



@permission_required('qualification.delete_categorylevel')
def delete_categorylevel(request,id):
    record = get_object_or_404(Categorylevel, id=id)
    write_to_file(request.user,"Categorylevel deleted Successfully!",record.id)
    levels=Qualification.objects.filter(level_id=record.id).count()
    if levels == 0:
        record.delete()
        messages.success(request, "Categorylevel deleted successfully!")
    else:
        messages.error(request, "This Category cannot be deleted now!")
    return redirect('/qualification/categorylevels')