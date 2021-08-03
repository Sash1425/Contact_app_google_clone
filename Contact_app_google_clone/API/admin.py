from django.contrib import admin
from  .models import Consumer, ContactDetails, Spam
# Register your models here.

admin.site.register(Consumer)
admin.site.register(ContactDetails)
admin.site.register(Spam)