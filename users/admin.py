from django.contrib import admin
from .models import Person, Company, Job, Application

admin.site.register(Person)
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Application)