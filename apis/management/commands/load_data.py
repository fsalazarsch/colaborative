from django.core.management.base import BaseCommand, CommandError
from map.models import Geodata
import sys

#
#from https://docs.djangoproject.com/en/1.8/howto/custom-management-commands/
#

class Command(BaseCommand):
  help = 'load data from text files'

  def add_arguments(self, parser):
    parser.add_argument('filepath', nargs=1, type=str)

  def handle(self, *args, **options):
    filepath = options['filepath'][0]
    fr = open(filepath, 'r')
    data = fr.read().strip().replace('\r','').replace('\t\n','\n').replace('\t\n','\n').split('\n')
    data = list(map(lambda x: x.split('\t'), data))
    names = data[0]
    names = list(map(lambda x: x.lower(), names))
    data = data[1:]
    for i in range(len(data)):
      cur = data[i]
      geocode = transformgeocode(cur[0])
      try:
        gd = Geodata.objects.get(geocode=geocode)
        for j in range(1,len(names)):
          gd.up_var(names[j], cur[j])
          gd.save()
          #print(gd.geocode, names[j], cur[j])
      except Exception as e:
        print(i, geocode, e)



def transformgeocode(string):
  if string[:3] == '056':
    return '2'+string[3:]
  else:
    return string
  
