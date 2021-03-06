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
    """
    Displays the home page 
    (called home to avoid overlap with the Django admin index page
    """

    context = {

    }
    return render(request, 'home.html', context = context)


class Results(LoginRequiredMixin, generic.ListView):
    """Fetches search results based on queries and relevant book sites"""
    queryset = SiteBookData
    template_name = 'results.html'

    def get_context_data(self, *args, **kwargs):
        """Gets search results from all sites the company is interested in """
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
        if author_list != None and author_list != '':
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
def book_detail(request, site, book_id):
    """Displays data for a single book"""
    base_site = checkmate.get_book_site(site)
    book_data = base_site.get_book_data_from_site(base_site.base + book_id)
    
    book_title = book_data.title
    book_subtitle = book_data.subtitle
    book_series = book_data.series
    book_authors = book_data.authors
    book_format = book_data.book_format
    book_ISBN = book_data.isbn_13
    book_url = book_data.url
    #book_match_percentage = "a fancy number"
    book_description = book_data.description
    book_ready_for_sale = book_data.ready_for_sale_string()

    context = {
        'book_title': book_title,
        'book_subtitle': book_subtitle,
        'book_series': book_series,
        'book_authors': book_authors,
        'book_format': book_format,
        'book_ISBN': book_ISBN,
        'book_url': book_url,
        #'book_match_percentage': book_match_percentage,
        'book_description': book_description,
        'book_ready_for_sale': book_ready_for_sale,
    }
    return render(request, 'book_detail.html', context = context)


class CompanyDetail(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing companies, their users, and their search counts"""
    model = Company
    template_name = 'company_detail.html'
    paginate_by = 3

    def get_queryset(self):
        """Returns the company the user is a part of, or all companies for unafiliated admins """
        u = self.request.user

        if u.is_staff:
            return Company.objects.order_by('company_name')
        elif u.person is not None:
            return Company.objects.filter(company_name=u.person.company).order_by('company_name')
        else: return None


@api_view(['POST'])
def search_books(request):
    """
    If user can be authenticated, then use checkmate to search for books. If the user is a customer, track search for billing purposes.

    request.body needs to be of the following form:

        username:"username",
        password:"password",
        queries:"[ {"author": "first author's name", "title": "first book title", "isbn": "first isbn"},
                    {"author": "second author's name", "title": "second book title", "isbn": "second isbn"},
                    .
                    .
                    .
                    {"author": "last author's name", "title": "last book title", "isbn": "last isbn"} ]"

    such that the array must contain at least one element and at least one field of at least one element must not be the empty sting
    (if the array is empty or every element contains only empty strings in its fields,
            no meaningful results will be returned but the user (if the user is a client and not an admin) will still be billed for that search)
    """
    
    un = request.body.username
    pw = request.body.password
    user = authenticate(username=un, password=pw)    
    
    if user is not None: 
        req = copy.deepcopy(request)
        req.user = user

        if user.person is not None or user.is_staff:
            # increment search_count for billing purposes
            if user.person is not None:        
                user.person.search_count += 1
                user.person.save()

            search_results = __perform_search(req)
        
            if search_results is not None:
                return Response(search_results, status=200)
            else:
                return Response("\"results\":\"None\"", status=204)
        
    return HttpResponseForbidden


@login_required
def __perform_search(request):
    """Uses checkmate to search all applicable websites and return books that match the search queries"""
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
            tb_list = checkmate.get_book_site('tb').find_book_matches_at_site(query_list)
            tb_list.sort(reverse=True,key = lambda x: x[1]) # get the results into descending order of % match if they weren't already
            if len(tb_list) > 10:
                tb_list = tb_list[:10]  # get the top ten results
            results_dict["tb"] = tb_list

        if request.user.is_staff or request.user.person.company.wants_kb:
            kb_list = checkmate.get_book_site('kb').find_book_matches_at_site(query_list)
            kb_list.sort(reverse=True,key = lambda x: x[1]) # get the results into descending order of % match if they weren't already
            if len(kb_list) > 10:
                kb_list = kb_list[:10]  # get the top ten results
            results_dict["kb"] = kb_list

        if request.user.is_staff or request.user.person.company.wants_gb:
            gb_list = checkmate.get_book_site('gb').find_book_matches_at_site(query_list)
            gb_list.sort(reverse=True,key = lambda x: x[1]) # get the results into descending order of % match if they weren't already
            if len(gb_list) > 10:
                gb_list = gb_list[:10]  # get the top ten results
            results_dict["gb"] = gb_list

        if request.user.is_staff or request.user.person.company.wants_lc:
            lc_list = checkmate.get_book_site('lc').find_book_matches_at_site(query_list)
            lc_list.sort(reverse=True,key = lambda x: x[1]) # get the results into descending order of % match if they weren't already
            if len(lc_list) > 10:
                lc_list = lc_list[:10]  # get the top ten results
            results_dict["lc"] = lc_list

        if request.user.is_staff or request.user.person.company.wants_sd:
            sd_list = checkmate.get_book_site('sd').find_book_matches_at_site(query_list)
            sd_list.sort(reverse=True,key = lambda x: x[1]) # get the results into descending order of % match if they weren't already
            if len(sd_list) > 10:
                sd_list = sd_list[:10]  # get the top ten results
            results_dict["sd"] = sd_list

        #convert the dictionary of lists into a JSON string & return it
        json_results = __jsonify_dict(results_dict)
        return json_results

    else:
        return None


@login_required
def __jsonify_dict(request, results_dict):
    """
    Accepts a dictionary where keys are site names and values are search results from those websites.
    Converts SiteBookData objects into JSON string, which is then returned.
    """
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

    # remove the trailing comma before closing the JSON string & returning
    last_comma_index = len(json_results) - 1
    json_results = json_results[:last_comma_index]
    json_results += "] }"
    return json_results