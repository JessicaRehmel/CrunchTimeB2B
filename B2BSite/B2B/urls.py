from django.urls import path
from . import views
from django.views.generic import RedirectView


urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'), #parses either the datafields or the JSON blob (throws an error if both or neither is given) and shows the results
    #path('book_detail/<slug:book_id>/', views.view_book_detail, name='view_book_detail'), #shows the comparison % and details on a given book???
    path('company_detail/', views.CompanyDetail.as_view(), name='company_detail'), #shows the reporting data for the company according to who is viewing the page
    path('admin/', RedirectView.as_view(url='admin/', permanent=True), name = 'admin'), #to give logged-in admins a direct link to the django-admin site
]