from django.shortcuts import render
from B2B.models import Company, Person
from django.views import generic

# Create your views here.

def index(request):
    """home/search page"""
    #we shouldn't have to do much here, since the search_results view will handle processing the form
    return render(request, 'index.html')

def query_results(request):
    #take the author/title/isbn and plug it into each of the checkmate parsers the user's company cares about, and display a list of SiteBookData objects
    return render(request, 'results.html')

def blob_results(request):
    #parse the JSON blob into author/title/isbn units, then plug each into each of the checkmate parsers the user's company cares about, and display a list of SiteBookData objects
    return render(request, 'results.html')