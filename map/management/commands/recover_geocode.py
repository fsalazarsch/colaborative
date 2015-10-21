from django.core.management.base import BaseCommand, CommandError
from project.models import Point
from map.models import Geocode
from map.utils import get_area_id, get_precision
import sys

#
#from https://docs.djangoproject.com/en/1.8/howto/custom-management-commands/
#

class Command(BaseCommand):
  help = 'Compute the geocode for a point (lat,lon) and save it'

  def add_arguments(self, parser):
    parser.add_argument('point_id', nargs=1, type=int)

  def handle(self, *args, **options):
    point_id = options['point_id'][0]
    point = Point.objects.get(pk=point_id)
    area_id = get_area_id(point.latitude, point.longitude)
    #print(area_id)
    geos = Geocode.objects.filter(area_id=area_id)

    for g in geos:
      if g.point_inside([point.latitude, point.longitude]):
        point.geocode = g.geocode
        point.save()
        sys.exit()

    aux = area_id.split('_')
    p = 1.0/10**get_precision()
    neighbours = []
    neighbours.append([point.latitude + p, point.longitude    ])
    neighbours.append([point.latitude + p, point.longitude + p])
    neighbours.append([point.latitude    , point.longitude + p])
    neighbours.append([point.latitude - p, point.longitude + p])
    neighbours.append([point.latitude - p, point.longitude    ])
    neighbours.append([point.latitude - p, point.longitude - p])
    neighbours.append([point.latitude    , point.longitude - p])
    neighbours.append([point.latitude + p, point.longitude - p])

    neighbours = [get_area_id(n[0], n[1]) for n in neighbours]
    for n in neighbours:
      geos = Geocode.objects.filter(area_id=n)
      for g in geos:
        if g.point_inside([point.latitude, point.longitude]):
          point.geocode = g.geocode
          point.save()
          sys.exit()

    neighbours = []
    neighbours.append([point.latitude + 2*p, point.longitude  ])
    neighbours.append([point.latitude + 2*p, point.longitude -1*p])
    neighbours.append([point.latitude + 2*p, point.longitude -2*p])
    neighbours.append([point.latitude +   p, point.longitude -2*p])
    neighbours.append([point.latitude      , point.longitude -2*p])
    neighbours.append([point.latitude -   p, point.longitude -2*p])
    neighbours.append([point.latitude - 2*p, point.longitude -2*p])
    neighbours.append([point.latitude - 2*p, point.longitude -  p])
    neighbours.append([point.latitude - 2*p, point.longitude     ])
    neighbours.append([point.latitude - 2*p, point.longitude +  p])
    neighbours.append([point.latitude - 2*p, point.longitude +2*p])
    neighbours.append([point.latitude -   p, point.longitude +2*p])
    neighbours.append([point.latitude      , point.longitude +2*p])
    neighbours.append([point.latitude +   p, point.longitude +2*p])
    neighbours.append([point.latitude + 2*p, point.longitude +2*p])
    neighbours.append([point.latitude + 2*p, point.longitude +  p])

    #more neighbours??
    neighbours = [get_area_id(n[0], n[1]) for n in neighbours]
    for n in neighbours:
      geos = Geocode.objects.filter(area_id=n)
      for g in geos:
        if g.point_inside([point.latitude, point.longitude]):
          point.geocode = g.geocode
          point.save()
          sys.exit()


    neighbours = []
    neighbours.append([point.latitude - 3*p, point.longitude + 3*p])
    neighbours.append([point.latitude - 2*p, point.longitude + 3*p])
    neighbours.append([point.latitude -   p, point.longitude + 3*p])
    neighbours.append([point.latitude      , point.longitude + 3*p])
    neighbours.append([point.latitude +   p, point.longitude + 3*p])
    neighbours.append([point.latitude + 2*p, point.longitude + 3*p])
    neighbours.append([point.latitude + 3*p, point.longitude + 3*p])

    neighbours.append([point.latitude + 3*p, point.longitude + 2*p])
    neighbours.append([point.latitude + 3*p, point.longitude +   p])
    neighbours.append([point.latitude + 3*p, point.longitude      ])
    neighbours.append([point.latitude + 3*p, point.longitude -   p])
    neighbours.append([point.latitude + 3*p, point.longitude - 2*p])
    neighbours.append([point.latitude + 3*p, point.longitude - 3*p])

    neighbours.append([point.latitude + 2*p, point.longitude - 3*p])
    neighbours.append([point.latitude +   p, point.longitude - 3*p])
    neighbours.append([point.latitude      , point.longitude - 3*p])
    neighbours.append([point.latitude -   p, point.longitude - 3*p])
    neighbours.append([point.latitude - 2*p, point.longitude - 3*p])
    neighbours.append([point.latitude - 3*p, point.longitude - 3*p])

    neighbours.append([point.latitude - 3*p, point.longitude - 3*p])
    neighbours.append([point.latitude - 3*p, point.longitude - 2*p])
    neighbours.append([point.latitude - 3*p, point.longitude -   p])
    neighbours.append([point.latitude - 3*p, point.longitude      ])
    neighbours.append([point.latitude - 3*p, point.longitude +   p])
    neighbours.append([point.latitude - 3*p, point.longitude + 2*p])

    #more neighbours??
    neighbours = [get_area_id(n[0], n[1]) for n in neighbours]
    for n in neighbours:
      geos = Geocode.objects.filter(area_id=n)
      for g in geos:
        if g.point_inside([point.latitude, point.longitude]):
          point.geocode = g.geocode
          point.save()
          sys.exit()

