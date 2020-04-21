from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import generics, renderers, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Company, Person

import requests
import sys
sys.path.append('.\..\checkmate')
import checkmate
from checkmate import SiteBookData
# Create your views here.

@login_required
def home(request):

    #print(checkmate.get_book_site('lc').slug)

    context = {

    }
    return render(request, 'home.html', context = context)

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

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def book_search(request):
    """request_body needs to be of the following form:

            "queries": [ 
                        {"author": "first author's name", "title": "first book title", "isbn": "first isbn"},
                        {"author": "second author's name", "title": "second book title", "isbn": "second isbn"},
                        .
                        .
                        .
                        {"author": "last author's name", "title": "last book title", "isbn": "last isbn"}
                    ]

        such that the array must contain at least one element and at least one field of at least one element must not be the empty sting
        (if the array is empty or every element contains only empty strings in its fields,
                no meaningful results will be returned but the user (if the user is a client and not an admin) will still be billed for that search)
    """
    if request.user.is_staff or request.user.person is not None:        
        if not request.user.is_staff:
            request.user.person.search_count += 1
            request.user.person.save()
        
        queries = request.body.queries
        search_results = perform_search(queries) #get the list of SiteBookData objects that match the search queries
        
        if search_results is not None:
            json_result = "results: ["
            
            for book in search_results:
                json_results.append(book.to_json(), ",")
            
            json_result.append("]")

            return response(json_result, status=200)

        else:
           res = response("\"results\":\"None\"", status=204)

        return res

    else:
        return HttpResponseForbidden

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
        KB_list = checkmate.get_book_site('kb').find_book_matches_at_site(book_data)
        GB_toggle = False
        GB_list = checkmate.get_book_site('gb').find_book_matches_at_site(book_data)
        LC_toggle = True
        LC_list = checkmate.get_book_site('lc').find_book_matches_at_site(book_data)
        SD_toggle = False
        SD_list = checkmate.get_book_site('sd').find_book_matches_at_site(book_data)
        TB_toggle = False
        TB_list = checkmate.get_book_site('tb').find_book_matches_at_site(book_data)

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
        context['TB_toggle'] = TB_toggle
        context['TB_list'] = TB_list
        return context

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
