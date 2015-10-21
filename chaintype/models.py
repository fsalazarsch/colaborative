from django.db import models


class ChainType(models.Model):
  name = models.CharField(max_length=254)

  def __str__(self):
    return str(self.name)


class ChainSubType(models.Model):
  chaintype = models.ForeignKey(ChainType)
  name = models.CharField(max_length=254)

  def __str__(self):
    return str(self.name)


