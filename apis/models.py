from django.db import models
from login.utils import now

class GooglePlaceCategory(models.Model):
  name = models.CharField(max_length=63)
  required = models.BooleanField(default=False)


class GooglePlace(models.Model):
  googleplacecategory = models.ForeignKey(GooglePlaceCategory, default=-1)
  latitude = models.FloatField(default=-200, db_index=True)
  longitude = models.FloatField(default=-200, db_index=True)
  google_id = models.CharField(max_length=63)
  google_place_id = models.CharField(max_length=63)
  datetime = models.DateTimeField(default=now())


class GooglePlaceRequest(models.Model):
  url = models.TextField()
  json = models.TextField()
  datetime = models.DateTimeField(default=now())
   
