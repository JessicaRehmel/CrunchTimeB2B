from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Company, Person

import requests
import sys
sys.path.append('.\..\checkmate')
import checkmate
from checkmate import SiteBookData
#from .checkmate import *
# Create your views here.

@login_required
def index(request, form_exception=None):

    #print(checkmate.get_book_site('lc').slug)

    context = {

    }
    return render(request, 'index.html', context = context)

@login_required
def check_form_data(request):
    book_title = request.GET.get("title_field")
    author_list = request.GET.get("author_field")
    book_ISBN = request.GET.get("ISBN_field")
    book_JSON = request.GET.get("JSON_field")
    
    if book_JSON != '':
        if book_title == '' and author_list == '' and book_ISBN == '':
            return #search with only JSON
        else:
            return #home(request, "JSON only or not") #to home with must search by JSON only or not error
    else:
        if book_title == '' and author_list == '' and book_ISBN == '':
            return #to home with empty exception
        else:
            return #search using only non-JSON
    

class Results(LoginRequiredMixin, generic.ListView):
    queryset = SiteBookData
    template_name = 'results.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        book_title = self.request.GET.get("title_field")
        author_list = self.request.GET.get("author_field")
        book_authors = []
        temp = ""
        if author_list != None:
            for letter in author_list:
                if letter == ",":
                    book_authors.append(temp)
                    temp = ""
                else:
                    temp = temp + letter
            book_authors.append(temp)
        book_ISBN = self.request.GET.get("ISBN_field")
        #book_match_percentage = self.request.GET.get("isbn_field")
        book_JSON = self.request.GET.get("JSON_field")

        book_data = SiteBookData(book_ISBN, book_title, book_authors)

        #needs to come from active company
        KB_toggle = True
        #KB_list = [["a title", ["maybe authors list", "a second auth"], "dat number yo", "dat fancy number yo"], ["a title2", ["maybe authors list2"], "dat number yo2", "dat fancy number yo2"]]
        KB_list = checkmate.get_book_site('kb').find_book_matches_at_site(book_data)
        GB_toggle = False
        GB_list = []
        LC_toggle = False
        LC_list = []
        SD_toggle = False
        SD_list = []

        context['book_title'] = book_title
        context['book_authors'] = book_authors
        context['book_ISBN'] = book_ISBN
        context['book_JSON'] = book_JSON
        context['KB_toggle'] = KB_toggle
        context['KB_list'] = KB_list
        context['GB_toggle'] = GB_toggle
        context['GB_list'] = GB_list
        context['LC_toggle'] = LC_toggle
        context['LC_list'] = LC_list
        context['SD_toggle'] = SD_toggle
        context['SD_list'] = SD_list
        return context

@login_required
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
            return Company.objects.filter(company_name=u.person.company).order_by('company_name')
        else: return None
