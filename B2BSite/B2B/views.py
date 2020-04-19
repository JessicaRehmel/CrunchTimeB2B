from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Company, Person

import requests
# Create your views here.

@login_required
def index(request):
    #all_books = Book.objects.all().order_by('title')

    context = {
        #'all_books': all_books,
    }
    return render(request, 'index.html', context = context)

@login_required
def results(request):
    #all_books = Book.objects.all().order_by('title')

    context = {
        #'all_books': all_books,
    }
    return render(request, 'results.html', context = context)

@login_required
def book_detail(request):
    #all_books = Book.objects.all().order_by('title')

    context = {
        #'all_books': all_books,
    }
    return render(request, 'book_detail.html', context = context)

class CompanyDetail(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing companies, their users, and their search counts"""
    model = Company
    template_name = 'company_detail.html'
    paginate_by = 3

    def get_queryset(self):
        u = self.request.user

        if u.is_staff:
            return Company.objects.order_by('company_name')
        elif u.person is not None:
            return Company.objects.filter(pk=u.person.company).order_by('company_name')
        else: return None
