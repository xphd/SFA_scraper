from django.db import models
from django.utils.translation import ugettext as _
from django_localflavor_us.models import USStateField

class Company(models.Model):
    name = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=255, primary_key=True)
    city = models.CharField(max_length=10, blank=True)
    state = USStateField(_("state"), default=" ")
    zipcode = models.CharField(_("zip code"), max_length=5, default=" ")
    owner_email = models.EmailField(blank=True)
    owner_Name = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank = True)
    datetime = models.CharField(max_length=100, blank = True)
    class Meta:
        unique_together = (('name', 'url'),)
    def __str__(self):
        return self.name

class CheckListLogs(models.Model):

    datetime = models.DateTimeField(auto_now=True)
    file_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=50)
    team = models.CharField(max_length=25)
    status = models.CharField(max_length=15)
    file_length = models.IntegerField()

class UploadListLogs(models.Model):

    datetime = models.DateTimeField(auto_now=True)
    file_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=50)
    team = models.CharField(max_length=25)
    upload_type = models.CharField(max_length=10)
    file_length = models.IntegerField()
