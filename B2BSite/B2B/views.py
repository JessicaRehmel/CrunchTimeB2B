from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
import requests
# Create your views here.

def index(request):
    #all_books = Book.objects.all().order_by('title')

    context = {
        #'all_books': all_books,
    }
    return render(request, 'index.html', context = context)

    
def results(request):
    book_title = "stuff"
    book_authors = "list of stuff"
    book_ISBN = "a long number"
    book_match_percentage = "a fancy number"
    #book_JSON = "dear lord the text"

    KB_toggle = True
    KB_list = [["a title", ["maybe authors list", "a second auth"], "dat number yo", "dat fancy number yo"], ["a title2", ["maybe authors list2"], "dat number yo2", "dat fancy number yo2"]]
    GB_toggle = False
    GB_list = []
    LC_toggle = False
    LC_list = []
    SC_toggle = False
    SC_list = []

    context = {
        'book_title': book_title,
        'book_authors': book_authors,
        'book_ISBN': book_ISBN,
        'book_match_percentage': book_match_percentage,
        #'book_JSON': book_JSON,
        'KB_toggle': KB_toggle,
        'KB_list': KB_list,
        'GB_toggle': GB_toggle,
        'GB_list': GB_list,
        'LC_toggle': LC_toggle,
        'LC_list': LC_list,
        'SC_toggle': SC_toggle,
        'SC_list': SC_list,
    }
    return render(request, 'results.html', context = context)


def book_detail(request):
    book_title = "stuff"
    book_subtitle = "lesser stuff"
    book_series = "even lesser stuff"
    book_volume = "a number"
    book_authors = "a list of stuff"
    book_format = "fancy stuff"
    book_ISBN = "a long number"
    book_url = "complex stuff"
    book_match_percentage = "a fancy number"
    book_description = "dear lord the text"

    context = {
        'book_title': book_title,
        'book_subtitle': book_subtitle,
        'book_series': book_series,
        'book_volume': book_volume,
        'book_authors': book_authors,
        'book_format': book_format,
        'book_ISBN': book_ISBN,
        'book_url': book_url,
        'book_match_percentage': book_match_percentage,
        'book_description': book_description,
    }
    return render(request, 'book_detail.html', context = context)


def company_detail(request):
    #all_books = Book.objects.all().order_by('title')

    context = {
        #'all_books': all_books,
    }
    return render(request, 'results.html', context = context)
