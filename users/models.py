from django.contrib.auth.models import User
from django.db import models
from multiselectfield import MultiSelectField


FIELDS_CHOICES = (
    ('P', 'Programmer'),
    ('D', 'Digial Marketing'),
    ('A', 'Architectural'),
    ('O', 'Other')
)


class Person(models.Model):
    user = models.OneToOneField(User, related_name = 'person', on_delete = models.CASCADE)
    firstname = models.CharField(max_length = 100)
    lastname = models.CharField(max_length = 100)
    birthday = models.DateField('birthday')
    gender = models.CharField(choices = (('M', 'Male'),('F', 'Female')), max_length = 1)
    field = MultiSelectField(choices = FIELDS_CHOICES, default = 0)
    dateofjoining = models.DateField(('dateofjoining'), auto_now_add = True)
    resume = models.ImageField(upload_to = 'Image/', null = True)


class Company(models.Model):
    user = models.OneToOneField(User, related_name = 'company', on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    creation_date = models.DateField('creation date')
    telephone_number = models.PositiveIntegerField()
    address = models.CharField(max_length = 100)
    dateofjoining = models.DateField(('dateofjoining'), auto_now_add = True)
    field = MultiSelectField(choices = FIELDS_CHOICES, default = 0)


class Job(models.Model):
    company = models.ForeignKey(Company, on_delete = models.CASCADE)
    title = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = 'Image/')
    create_date = models.DateField(('create_date'), auto_now_add = True)
    expire_date = models.DateField()
    field = models.CharField(choices = FIELDS_CHOICES, max_length = 1)
    salary = models.IntegerField(default = 0)
    working_hours = models.IntegerField()

    def __str__(self):
        return self.title + "-" + self.company.name


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete = models.CASCADE)
    person = models.ForeignKey(Person, on_delete = models.CASCADE)