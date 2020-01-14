from django.db import models
from datetime import datetime


class Contact(models.Model):
    listing = models.CharField(max_length=200)
    listing_id = models.IntegerField()
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    contact_date = models.DateField(default=datetime.now, blank=True)
    user_id = models.IntegerField(blank=True)

    def __str__(self):
        return self.name


class Inquiry(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=30, blank=True)
    ref_id = models.CharField(max_length=30)
    headline = models.CharField(max_length=400)
    nda_sent = models.BooleanField(default=False)
    last_updated = models.DateField(default=datetime.now, blank=True)
