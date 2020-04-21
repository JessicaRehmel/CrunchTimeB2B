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
def home(request):

    context = {

    }
    return render(request, 'home.html', context = context)

    

class Results(LoginRequiredMixin, generic.ListView):
    queryset = SiteBookData
    template_name = 'results.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.request.user
        company = user.person.company
        if user.person != None:
            user.person.search_count += 1
            user.person.save()

        book_title = self.request.GET.get("title_field")
        author_list = self.request.GET.get("authors_field")
        book_ISBN = self.request.GET.get("ISBN_field")
        book_JSON = self.request.GET.get("JSON_field")
        error_message = ''

        q = ""
        if book_title:
            q = q + book_title
        if author_list:
            q = q + author_list
        if book_ISBN:
            q = q + book_ISBN
        #JSON stuff?

        #testing this
        if book_JSON != '':
            if book_title == '' and author_list == '' and book_ISBN == '':
                pass #searching with only JSON
            else:
                context['error_message'] = "You must enter only JSON data OR title, author, and/or ISBN information into the search fields. Return Home to retry." #to home with must search by JSON only or not error
                return context
        else:
            if book_title == '' and author_list == '' and book_ISBN == '':
                context['error_message'] = "Search fields were left blank. Please return to Home and enter search information." #to home with empty exception
                return context
            else:
                pass #search using only non-JSON
        
        
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
        

        book_data = SiteBookData(book_ISBN, book_title, book_authors)

        #needs to come from active company
        if company.wants_kb:
            KB_list = checkmate.get_book_site('kb').find_book_matches_at_site(book_data)
            if len(KB_list) > 10:
                KB_list = KB_list[:10]
            KB_list.sort(reverse=True,key = lambda x: x[1])  
            context['KB_list'] = KB_list
        if company.wants_gb:
            GB_list = checkmate.get_book_site('gb').find_book_matches_at_site(book_data)
            if len(GB_list) > 10:
                GB_list = GB_list[:10]
            GB_list.sort(reverse=True,key = lambda x: x[1])  
            context['GB_list'] = GB_list
        if company.wants_lc:
            LC_list = checkmate.get_book_site('lc').find_book_matches_at_site(book_data)
            if len(LC_list) > 10:
                LC_list = LC_list[:10]
            LC_list.sort(reverse=True,key = lambda x: x[1])  
            context['LC_list'] = LC_list
        if company.wants_sd:
            SD_list = checkmate.get_book_site('sd').find_book_matches_at_site(book_data)
            if len(SD_list) > 10:
                SD_list = SD_list[:10]
            SD_list.sort(reverse=True,key = lambda x: x[1])  
            context['SD_list'] = SD_list
        if company.wants_tb:
            TB_list = checkmate.get_book_site('tb').find_book_matches_at_site(book_data)
            if len(TB_list) > 10:
                TB_list = TB_list[:10]
            TB_list.sort(reverse=True,key = lambda x: x[1])  
            context['TB_list'] = TB_list

        context['search_terms'] = q
        context['book_title'] = book_title
        context['book_authors'] = book_authors
        context['book_ISBN'] = book_ISBN
        context['book_JSON'] = book_JSON
        context['KB_toggle'] = company.wants_kb
        context['GB_toggle'] = company.wants_gb
        context['LC_toggle'] = company.wants_lc
        context['SD_toggle'] = company.wants_sd
        context['TB_toggle'] = company.wants_tb
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
