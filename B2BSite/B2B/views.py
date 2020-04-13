from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
# Create your views here.

def index(request):
    #all_books = Book.objects.all().order_by('title')

    context = {
        #'all_books': all_books,
    }
    return render(request, 'index.html', context = context)