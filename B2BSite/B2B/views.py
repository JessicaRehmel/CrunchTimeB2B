from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
import requests
import sys
sys.path.append('.\..\checkmate')
import checkmate
#from .checkmate import *
# Create your views here.

def index(request):
    #all_books = Book.objects.all().order_by('title')

    print(checkmate.get_book_site('lc').slug)

    context = {
        #'all_books': all_books,
    }
    return render(request, 'index.html', context = context)

    
def results(request):
    #all_books = Book.objects.all().order_by('title')

    context = {
        #'all_books': all_books,
    }
    return render(request, 'results.html', context = context)


def book_detail(request):
    #all_books = Book.objects.all().order_by('title')

    context = {
        #'all_books': all_books,
    }
    return render(request, 'book_detail.html', context = context)


def company_detail(request):
    #all_books = Book.objects.all().order_by('title')

    context = {
        #'all_books': all_books,
    }
    return render(request, 'company_detail.html', context = context)
