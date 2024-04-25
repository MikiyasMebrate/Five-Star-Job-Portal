from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from Company.models import (Company)
from Company.forms import (CompanyForm)
# Create your views here.
def index(request):
    return render(request, 'UserAdmin/index.html')

def company(request, id=None):
    form = CompanyForm(request.POST or None, request.FILES or None)
    companies = Company.objects.all()
    count = 30
    paginator = Paginator(companies, 30) 
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
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating Company')

    
    context = {
        'companies' : page,
        'count' : count,
        'form' : form
    }
    return render(request, 'UserAdmin/company.html', context=context)
    

    

def company_detail(request, id):
    try:
        company = Company.objects.get(pk = id)
    except:
        company = None
    
    form = CompanyForm(request.POST or None, request.FILES or None, instance=company)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
            return redirect('user-admin-company-detail',f'{id}')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating Company')
    context = {
        'form': form
    }
    return render(request, 'UserAdmin/company_detail.html', context=context)

def company_delete(request, id):
    try:
        company = Company.objects.get(pk = id)
        company.delete()
        messages.success(request, '&#128515 Hello User, Successfully Deleted')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting Company')
    
    return redirect('user-admin-company')

