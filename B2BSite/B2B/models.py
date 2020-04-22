from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):

    company_name = models.CharField(max_length=100)
    primary_contact = models.ForeignKey('Person', related_name='+', blank=True, null=True, on_delete=models.SET_NULL)

    wants_tb = models.BooleanField(verbose_name='can search Test Bookstore (for TESTING purposes ONLY)') #NO REAL COMPANY WILL WANT THIS
    wants_kb = models.BooleanField(verbose_name='can search Kobo')
    wants_gb = models.BooleanField(verbose_name='can search Google Books')
    wants_lc = models.BooleanField(verbose_name='can search Livraria Cultura')
    wants_sd = models.BooleanField(verbose_name='can search Scribd')

    def get_total_searches(self):
        total = 0
        for p in self.person_set.all():
            total = total + p.search_count
        return total

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = "Companies"

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name='User Account') #disallow deletion of users; for auditing purposes it's safer to just go into the admin & uncheck "Active" for the user
    company =  models.ForeignKey('Company', on_delete=models.PROTECT) #disallow deletion of companies; for auditing purposes it's safer to just deactivate all users at the company
    phone = models.CharField(max_length=20, blank=True) #20 chars allows international numbers which can be long, nullable because not everyone has a phone number we care about
    search_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name + " " +  self.user.last_name
