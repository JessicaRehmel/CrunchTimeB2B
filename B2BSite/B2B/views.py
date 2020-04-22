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

    context = {

    }
    return render(request, 'home.html', context = context)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def perform_search(request):
    if request.user.is_staff or request.user.person is not None:
        if request.body.queries:
            # convert the JSON queries into a list of partial SiteBookData objects
            query_list = []
            for q in request.body.queries:
                query = SiteBookData()
                query.from_json(q)
                query_list.append(query)

            #use the checkmate scrapers to get the results from all applicable sites
            results_dict = {}

            if request.user.is_staff or request.user.person.company.wants_tb:
                tb_list = checkmate.get_book_site('tb').find_book_matches_at_site(book_data)
                tb_list.sort(reverse=True,key = lambda x: x[1]) # get the results into descending order of % match if they weren't already
                if len(tb_list) > 10:
                    tb_list = tb_list[:10]  # get the top ten results
                results_dict["tb"] = tb_list

            if request.user.is_staff or request.user.person.company.wants_kb:
                kb_list = checkmate.get_book_site('kb').find_book_matches_at_site(book_data)
                kb_list.sort(reverse=True,key = lambda x: x[1]) # get the results into descending order of % match if they weren't already
                if len(kb_list) > 10:
                    kb_list = kb_list[:10]  # get the top ten results
                results_dict["kb"] = kb_list

            if request.user.is_staff or request.user.person.company.wants_gb:
                gb_list = checkmate.get_book_site('gb').find_book_matches_at_site(book_data)
                gb_list.sort(reverse=True,key = lambda x: x[1]) # get the results into descending order of % match if they weren't already
                if len(gb_list) > 10:
                    gb_list = gb_list[:10]  # get the top ten results
                results_dict["gb"] = gb_list

            if request.user.is_staff or request.user.person.company.wants_lc:
                lc_list = checkmate.get_book_site('lc').find_book_matches_at_site(book_data)
                lc_list.sort(reverse=True,key = lambda x: x[1]) # get the results into descending order of % match if they weren't already
                if len(lc_list) > 10:
                    lc_list = lc_list[:10]  # get the top ten results
                results_dict["lc"] = lc_list

            if request.user.is_staff or request.user.person.company.wants_sd:
                sd_list = checkmate.get_book_site('sd').find_book_matches_at_site(book_data)
                sd_list.sort(reverse=True,key = lambda x: x[1]) # get the results into descending order of % match if they weren't already
                if len(sd_list) > 10:
                    sd_list = sd_list[:10]  # get the top ten results
                results_dict["sd"] = sd_list

            #convert the dictionary of lists into a JSON string
            json_results = "{ \"results\": ["

            if results_dict["tb"] is not None:
                l = results_dict["tb"]
                json_results += " { \"from Test Bookstore\": [ "                
                for e in l:
                    json_results += e.to_json()
                    if l.index_of(e) < len(l) - 1:
                        json_results += ","
                json_results += " ] },"

            if results_dict["kb"] is not None:
                l = results_dict["kb"]
                json_results += " {\"from Kobo\": [ "
                for e in l:
                    json_results += e.to_json()
                    if l.index_of(e) < len(l) - 1:
                        json_results += ","
                json_results += " ] },"

            if results_dict["gb"] is not None:
                l = results_dict["gb"]
                json_results += " {\"from Google Books\": [ "
                for e in l:
                    json_results += e.to_json()
                    if l.index_of(e) < len(l) - 1:
                        json_results += ","
                json_results += " ] },"

            if results_dict["lc"] is not None:
                l = results_dict["lc"]
                json_results += " {\"from Livraria Cultura\": [ "
                for e in l:
                    json_results += e.to_json()
                    if l.index_of(e) < len(l) - 1:
                        json_results += ","
                json_results += " ] },"

            if results_dict["sd"] is not None:
                l = results_dict["sd"]
                json_results += " {\"from Scribd\": [ "
                for e in l:
                    json_results += e.to_json()
                    if l.index_of(e) < len(l) - 1:
                        json_results += ","
                json_results += " ] },"

            # remove the trailing comma before closing the JSON string
            last_comma_index = len(json_results) - 1
            json_results = json_results[:last_comma_index]
            json_results += "] }"
            
            #send back the results string
            return json_results

        else:
            return None

        pass
    else:
        return None
    pass

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def book_search(request):
    """request.body needs to be of the following form:

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
            # we increment the counter here and not in perform_search because the logic is here and perform_search just does the heavy lifting
            request.user.person.search_count += 1
            request.user.person.save()
        
        search_results = perform_search(request) # get the JSON-ified list of book matches
        
        if search_results is not None:
            res = response(search_results, status=200)
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
                context['error_message'] = "You must enter only JSON data OR title, author, and/or ISBN information into the search fields. Return Home to retry."
                return context
        else:
            if book_title == '' and author_list == '' and book_ISBN == '':
                context['error_message'] = "Search fields were left blank. Please return to Home and enter search information."
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
            KB_list.sort(reverse=True,key = lambda x: x[1])  
            if len(KB_list) > 10:
                KB_list = KB_list[:10]
            context['KB_list'] = KB_list
        if company.wants_gb:
            GB_list = checkmate.get_book_site('gb').find_book_matches_at_site(book_data)
            GB_list.sort(reverse=True,key = lambda x: x[1])  
            if len(GB_list) > 10:
                GB_list = GB_list[:10]
            context['GB_list'] = GB_list
        if company.wants_lc:
            LC_list = checkmate.get_book_site('lc').find_book_matches_at_site(book_data)
            LC_list.sort(reverse=True,key = lambda x: x[1])  
            if len(LC_list) > 10:
                LC_list = LC_list[:10]
            context['LC_list'] = LC_list
        if company.wants_sd:
            SD_list = checkmate.get_book_site('sd').find_book_matches_at_site(book_data)
            SD_list.sort(reverse=True,key = lambda x: x[1])  
            if len(SD_list) > 10:
                SD_list = SD_list[:10]
            context['SD_list'] = SD_list
        if company.wants_tb:
            TB_list = checkmate.get_book_site('tb').find_book_matches_at_site(book_data)
            TB_list.sort(reverse=True,key = lambda x: x[1])  
            if len(TB_list) > 10:
                TB_list = TB_list[:10]
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
def book_detail(request, book_id):


    
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
