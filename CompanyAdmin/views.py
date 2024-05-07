from django.shortcuts import render, redirect, HttpResponse ,  get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from JobPortal.forms import (JobPostingCompanyAdminForm, ApplicationForm, AdminInterviewForm)
from JobPortal.models import ( Job_Posting, Application, Candidate, Education, Experience, Sector, Interviews)
from UserManagement.models import (CustomUser)
from django.db.models import Q
from django.contrib import messages 
from Company.models import Contact_Message , Company
from Company.forms import CompanyForm
from UserManagement.models import CustomUser 
from django.db.models import Count, Subquery
from UserManagement.forms import CustomUserCreationForm , CustomUserEditFormCompanyAdmin , CompanyAdmin , CustomUserEditFormAdmin , ChangePasswordForm
from UserManagement.decorators import (admin_user_required)
# Create your views here.

@admin_user_required
def index(request):
    total_users = CustomUser.objects.filter(company = request.user.company).count()
    total_views = request.user.company.views
    total_jobs = Job_Posting.objects.filter(company = request.user.company).count()
    total_applicant = Application.objects.filter(job__company = request.user.company).count()
    sectors_with_job_counts = Sector.objects.annotate(job_posting_count=Count('job_posting', filter=Q(job_posting__company=request.user.company))).order_by('-job_posting_count').values_list('name', 'job_posting_count')[:15]
    sectors_with_job_counts_lists = [list(ele) for ele in sectors_with_job_counts]



    context = {
        'total_users' : total_users,
        'total_views' : total_views,
        'total_jobs' : total_jobs,
        'total_applicant' : total_applicant,
        'sectors_with_job_counts_lists' : sectors_with_job_counts_lists
    }
    return render(request, 'CompanyAdmin/index.html', context=context)


@admin_user_required
def job_posting(request):
    form = JobPostingCompanyAdminForm(request.POST or None, request.FILES or None)
    jobs = Job_Posting.objects.filter(company = request.user.company)
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        jobs = Job_Posting.objects.filter( company = request.user.company).filter(Q(title__contains=q) | Q(sector__name__contains=q) | Q(salary_range_start__contains=q) | Q(salary_range_final__contains=q) | Q(type__contains=q))
    
    paginator = Paginator(jobs, 30) 
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
        except: count = (30 * (int(1) if page_number  else 1) ) - 30
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) - 30
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.company = request.user.company
            obj.save()
            form.save_m2m()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
            return redirect('company-admin-job-posting')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating Company')
            return redirect('company-admin-job-posting')
    
    
    context = {
        'jobs' : page,
        'count' : count,
        'form' : form,
    }
    return render(request, 'CompanyAdmin/job_posting.html', context=context)



@admin_user_required
def company_interviewer(request):
    user = request.user
    company = user.company
    form = CompanyAdmin(request.POST or None, request.FILES or None)
    company_interviewer = CustomUser.objects.filter(is_interviewer=True , company=company)
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        company_interviewer = CustomUser.objects.filter( Q(first_name__contains=q) |Q(last_name__contains=q) | Q(phone__icontains=q) | Q(email__icontains=q) , is_admin=True , company=company )
    
    paginator = Paginator(company_interviewer, 30) 
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
        except: count = (30 * (int(1) if page_number  else 1) ) - 30
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) - 30
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30

    if request.method == 'POST':
        if form.is_valid():
            x = form.save(commit=False)
            x.is_interviewer =True
            x.company = company
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Added')
            return redirect('company_interviewer')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Adding Company')
    

    
    context = {
        'company_interviewer' : page,
        'count' : count,
        'form' : form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'CompanyAdmin/company_interviewer.html', context=context)
    

@admin_user_required
def company_admins(request):
    user = request.user
    company = user.company
    form = CompanyAdmin(request.POST or None, request.FILES or None)
    company_admins = CustomUser.objects.filter(is_admin=True , company=company)
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        company_admins = CustomUser.objects.filter( Q(first_name__contains=q) |Q(last_name__contains=q) | Q(phone__icontains=q) | Q(email__icontains=q) , is_admin=True , company=company )
    
    paginator = Paginator(company_admins, 30) 
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
        except: count = (30 * (int(1) if page_number  else 1) ) - 30
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) - 30
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30

    if request.method == 'POST':
        if form.is_valid():
            x = form.save(commit=False)
            x.is_admin=True
            x.company = company
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Added')
            return redirect('company_admins')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Adding Company')
    

    
    context = {
        'company_admins' : page,
        'count' : count,
        'form' : form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'CompanyAdmin/company_admin_users.html', context=context)
    

    
@admin_user_required
def company_user_detail(request, id):
    try:
       company_admins  = CustomUser.objects.get(id=id , company=request.user.company)
    except:
        return HttpResponse('You are not authorized to access this page!')
    
    form = CustomUserEditFormCompanyAdmin(request.POST or None, request.FILES or None, instance=company_admins)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
            return redirect('company_admins')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating Company')
    context = {
        'form': form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'CompanyAdmin/company_admin_user_detail.html', context=context)


@admin_user_required
def company_user_delete(request, id):
    try:
        user = CustomUser.objects.get(pk = id, company=request.user.company)
    except:
        return HttpResponse('You are not authorized to access this page!')
    try:
        user.delete()
        messages.success(request, '&#128515 Hello User, Successfully Deleted')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting')
    
    return redirect('company_admins')

@admin_user_required
def change_status_user(request, id):
    user = CustomUser.objects.get(id=id)
    current_user = request.user
    if user != current_user: 
       if user.is_active:
           user.is_active = False
           user.save()
           return redirect('/') 
       else:
           user.is_active = True
           user.save()
           return redirect('/') 
    else :
        return error



    return redirect('/')   


@admin_user_required
def company_admin_profile(request):
    
    user = request.user
    form =  CustomUserEditFormAdmin(request.POST or None, request.POST or None, instance=user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Updating User Information ')

    context = {
        'user' : user,
        'form' : form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }

    return render(request, 'CompanyAdmin/profile.html', context=context)


@admin_user_required
def company_admin_change_password(request):
    form = ChangePasswordForm(request.user)
    if request.method == 'POST':
        form = ChangePasswordForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hello User,Password Successfully Updated')
            logout(request)
            return redirect('login')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Updating User Password! ')

    
    return render(request,'CompanyAdmin/change_password.html', {'form': form})  


    

@admin_user_required
def job_delete(request, id):
    try:
        job = Job_Posting.objects.get(pk = id, company=request.user.company)
    except:
        return HttpResponse('You are not authorized to access this page!')

    try:
        job.delete()
        messages.success(request, '&#128515 Hello User, Successfully Deleted')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting Company')
    
    return redirect('company-admin-job-posting')    

@admin_user_required
def job_detail(request, id):
    try:
        job = Job_Posting.objects.get(pk = id, company=request.user.company)
    except:
        return HttpResponse('You are not authorized to access this page!')
    
    form = JobPostingCompanyAdminForm(request.POST or None, request.FILES or None, instance=job)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            form.save_m2m()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
            return redirect('company-admin-job-posting')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating job')
    context = {
        'form': form,
    }
    return render(request, 'CompanyAdmin/job_detail.html', context=context)



@admin_user_required
def applicant(request):
    form = JobPostingCompanyAdminForm(request.POST or None, request.FILES or None)

    jobs = Application.objects.filter( job__company = request.user.company).select_related()
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        jobs = Application.objects.filter(job__company = request.user.company).filter(Q(user__first_name__contains=q) | Q(user__last_name__contains=q) | Q(user__phone__contains=q) | Q(user__email__contains=q) | Q(job__title__contains=q) | Q(date_applied__contains=q) | Q(status__contains=q)).select_related()
    
    paginator = Paginator(jobs, 30) 
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
        except: count = (30 * (int(1) if page_number  else 1) ) - 30
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) - 30
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.company = request.user.company
            obj.save()
            form.save_m2m()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
            return redirect('company-admin-job-posting')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating Company')
            return redirect('company-admin-job-posting')

    context = {
        'applications' : page,
        'count' : count,
        'form' : form,
    }
    return render(request, 'CompanyAdmin/applicant.html', context=context)



@admin_user_required
def applicant_detail(request, id, job_id, app_id):
   
    try:
        user = CustomUser.objects.get(pk = id)   
        education = Education.objects.filter(candidate = user).select_related()
        experience = Experience.objects.filter(candidate = user).select_related()
        job = Job_Posting.objects.get(pk = job_id)
        app = Application.objects.get(pk = app_id)
        interview = Interviews.objects.filter(application = app).first()
        form = ApplicationForm(request.POST or None, instance=app)

        try:
            interview_form = AdminInterviewForm(request.user.company, request.POST or None, instance=interview)
        except:
            interview_form = AdminInterviewForm(request.user.company, request.POST or None)

    except:
        return HttpResponse('You are not authorized to access this page!')
    
    if request.method == "POST":
        if 'status' in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, '&#128515 Hello User, Status successfully  updated')
                

        if 'interviewer' in request.POST:
            if interview_form.is_valid():
                obj = interview_form.save(commit=False)
                obj2 = form.save(commit=False)
                if interview_form.cleaned_data['interviewer'] is not None:
                    obj2.status = 'in_review'  
                else:
                    obj2.status = 'pending' 

                obj2.save()
                obj.application = app
                obj.save()
                messages.success(request, '&#128515 Hello User,  successfully  updated')
                return redirect('company-admin-applicant')
                
                
    context = {
        'user' : user,
        'education' : education,
        'experience' : experience,
        'job' : job,
        'form' : form,
        'interview_form' : interview_form,
    }
    return render(request, 'CompanyAdmin/applicant_detail.html', context=context)

@admin_user_required
def company_info (request):
    company = get_object_or_404(Company, id=request.user.company.id)
    context = {
        "company" : company
    }
    return render(request , 'CompanyAdmin/company_info.html' , context)


@admin_user_required
def edit_company_info (request , id):
    company = Company.objects.get(id=id)
    form = CompanyForm(request.POST or None, request.FILES or None, instance=company)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128515 Successfully Updated')
            return redirect('company_info')
        else:
            messages.error(request, '&#128532  An error occurred while updating Company')
            return redirect('company_info')
    context = {
        "company" : company,
        "form" : form
    }
    return render(request , 'CompanyAdmin/edit_company_info.html' , context)

    


