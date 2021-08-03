from django.db import models


# Create your models here.
class ContactDetails(models.Model):
    full_name = models.CharField(max_length=225, )
    phone_number = models.CharField(max_length=10)


class Consumer(models.Model):
    full_name = models.CharField(max_length=225)
    email = models.EmailField(max_length=225, blank=False)
    phone_number = models.ManyToManyField(ContactDetails)
    user = models.CharField(max_length=225)


class Spam(models.Model):
    phone_number = models.CharField(max_length=225)
    number_of_report = models.IntegerField()
