from django.db import models
from project.models import Point
from map.utils import point_in_poly, get_area_id, get_precision, centroid



class Geocode(models.Model):
  area_id = models.CharField(max_length=255, db_index=True)
  geocode = models.BigIntegerField()
  vertices = models.TextField()
  centroid_latitude = models.FloatField(default=-200, db_index=True)
  centroid_longitude = models.FloatField(default=-200, db_index=True)

  def __str__(self):
    return str(self.id)

  def point_inside(self, point):
    polygon = eval(self.vertices)
    return point_in_poly(point, polygon)



class Geodata(models.Model):
  geocode = models.BigIntegerField(db_index=True)
  var = models.TextField(null=True)

  #Geodata -> str
  def __str__(self):
    return str(self.geocode)

  #Geodata, str,
  def up_var(self, key, value):
    if self.var:
      var = eval(self.var)
      var[key] = value
      self.var = str(var)
    else:
      self.var = str({key:value})
    self.save()

  def get_var(self, key):
    if self.var:
      var = eval(self.var)
      if key in var:
        return var[key]
      else:
        return None
    else:
      return None

  def get_vars(self):
    if self.var:
      return eval(self.var)
    else:
      return None



class UrbanDataDescription(models.Model):
  code = models.CharField(max_length=31, db_index=True)
  name = models.CharField(max_length=63)
  description = models.CharField(max_length=255)


