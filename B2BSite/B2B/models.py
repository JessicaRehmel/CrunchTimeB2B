from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    primary_contact = models.ForeignKey(User, on_delete=models.SET_NULL)

    wants_tb = models.BooleanField() #do they care about the Test Bookstore; NO REAL COMPANY WILL - THIS IS JUST HERE FOR TESTING PURPOSES
    wants_kb = models.BooleanField() #do they care about Kobo
    wants_gb = models.BooleanField() #do they care about Google Books
    wants_lc = models.BooleanField() #do they care about Livraria Cultura
    wants_sd = models.BooleanField() #do they care about Scribd
    wants_ab = models.BooleanField() #do they care about Audiobooks.com

    def get_total_searches(self):
        for u in :


class CompanyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT) #disallow deletion of users; for auditing purposes it's safer to just go into the admin & remove the user's permissions
    company =  models.ForeignKey(Company, on_delete=models.PROTECT) #disallow deletion of companies; see previous comment
    phone = models.CharField(max_length=20, null=True) #20 chars allows international numbers which can be long, nullable because not every user has a phone number we care about
    search_count = models.IntegerField(default=0)
