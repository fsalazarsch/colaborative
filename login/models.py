from django.db import models
from django.contrib.auth.models import User
from project.models import Point, Project, ProjectUser, HitscoreModel
from login.utils import now


class ExceptionError(models.Model):
  app = models.CharField(max_length=255)
  view = models.CharField(max_length=255)
  datetime = models.DateTimeField(default=now())
  var = models.TextField(null=True)
  message = models.TextField(null=True)


class SimpleLog(models.Model):
  datetime = models.DateTimeField(default=now())
  category = models.CharField(max_length=255, null=True)
  message = models.TextField(null=True)



