from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    relevant_parsers = [] # figure out how to store a list of Checkmate parsers that will be activated if a user at the company runs a search


class CompanyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT) #disallow deletion of users; for auditing purposes it's safer to just go into the admin & remove the user's permissions
    company =  models.ForeignKey(Company, on_delete=models.PROTECT) #disallow deletion of companies; see previous comment
    search_count = models.IntegerField(default=0)
