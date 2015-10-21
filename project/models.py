from django.db import models
from django.contrib.auth.models import User
from login.utils import now

        
class Project(models.Model):
  name = models.CharField(max_length=255)
  computing_model = models.BooleanField(default=False)
  model_msg = models.CharField(max_length=255, default="Sorry, we still need more sales data for prediction (at least 3 locations)")
  updated = models.BooleanField(default=False)

  def __str__(self):
    return str(self.name)



class ProjectUser(models.Model):
  project = models.ForeignKey(Project, default=-1)
  user = models.ForeignKey(User, default=-1)
  permission = models.IntegerField(default=0) #0 owner; 1 read and write; 2 read only

  def __str__(self):
    return str(self.user) + ',' + str(self.project)



class Point(models.Model):
  project = models.ForeignKey(Project, default=-1)
  latitude = models.FloatField()
  longitude = models.FloatField()
  geocode = models.BigIntegerField(null=True)
  var = models.TextField(null=True, default='{}')
  urban_data = models.TextField(null=True, default='{}')
  sales = models.IntegerField(null=True) #yearly sales
  sales_index = models.FloatField(null=True)
  status = models.IntegerField(default=1) #1: Interested; 2: Confirm data; 3: In Negotiation; 4:Rejected; 5: Open; 6:Recomended
  opening_date = models.DateTimeField(null=True)
  square_feet = models.FloatField(null=True)
  opened_days = models.IntegerField(null=True)
  created_by = models.ForeignKey(User, null=True, related_name='created_by')
  edited_by = models.ForeignKey(User, null=True, related_name='edited_by')
  creation_date = models.DateTimeField(default=now)
  edition_date = models.DateTimeField(default=now)
  
  def get_readable_status(self):
    readable_status = { 1: "Interested",
                        2: "Confrim data",
                        3: "In negotiation",
                        4: "Rejected",
                        5: "Open",
                        6: "Recomended"}
    try:
      output = readable_status[self.status]
    except KeyError:
      output = "Undefined status"
    return output
      
  def get_hitscore_or_salesindex(self):
    if self.status == 5: #open
      if self.sales_index:
        return int(self.sales_index)
      return None
    return self.hitscore()

  def hitscore(self):
    try:
      hm = HitscoreModel.objects.get(project=self.project, valid=True)
      hv = HitscoreValue.objects.get(hitscoremodel=hm, point=self)
      return int(hv.value)
    except Exception as e:
      return None
    return None

  def __str__(self):
    return ','.join([str(self.project), str(self.latitude), str(self.longitude)])

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
    return None

  def get_vars(self):
    if self.var:
      return eval(self.var)
    return None


class HitscoreModel(models.Model):
  project = models.ForeignKey(Project, default=-1)
  formula = models.CharField(null=True, max_length=255)
  model = models.TextField(null=True) #{}
  msmm = models.TextField(null=True) #{}
  pca  = models.TextField(null=True) #{}
  rownamemsmm = models.TextField(null=True) #[]
  rownamepca = models.TextField(null=True) #[]
  attributes = models.TextField(null=True, default='[]') # [var_name] variables mas correlacionadas
  loocv_rmse = models.FloatField(null=True)
  loocv_mae = models.FloatField(null=True)
  modeling_time = models.FloatField(null=True)
  modeling_date = models.DateTimeField(default=now())
  valid = models.BooleanField(default=False)


class HitscoreValue(models.Model):
  hitscoremodel = models.ForeignKey(HitscoreModel, default=-1)
  point = models.ForeignKey(Point, default=-1)
  datetime = models.DateTimeField(default=now())
  value = models.FloatField(null=True)


class UsedPoint(models.Model):
  hitscoremodel = models.ForeignKey(HitscoreModel, default=-1)
  latitude = models.FloatField()
  longitude = models.FloatField()
  geocode = models.BigIntegerField(null=True)
  var_geocode = models.TextField(null=True, default='{}') 
  urban_data = models.TextField(null=True, default='{}')
  sales = models.IntegerField(null=True)


class Reports(models.Model):
  url_report = models.TextField()

