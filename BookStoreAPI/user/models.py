from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from book.models import Book

class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
   date_modified = models.DateTimeField(User, auto_now=True)
   phone = models.CharField(max_length=15, blank=True)
   address  = models.CharField(max_length=200, blank=True)
   old_cart = models.JSONField(default=list, null=True, blank=True)

   def __str__(self):
      return self