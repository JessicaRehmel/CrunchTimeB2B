from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
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

@login_required
def company_detail(request):
    #all_books = Book.objects.all().order_by('title')

    context = {
        #'all_books': all_books,
    }
    return render(request, 'company_detail.html', context = context)
