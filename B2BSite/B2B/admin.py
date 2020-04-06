from django.contrib import admin

from .models import Company, Person

class CompanyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Company)
admin.site.register(Person)
