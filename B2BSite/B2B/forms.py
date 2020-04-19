#this file may be deleted if the code does not see use in the final product
from django import forms

class SearchForm(forms.Form):
    search_title = forms.CharField(label='Title')
    search_authors = forms.CharField(label='Authors')
    search_ISBN = forms.CharField(label='ISBN')
    search_JSON = forms.CharField(label='JSON')