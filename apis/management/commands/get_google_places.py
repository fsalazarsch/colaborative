from django.core.management.base import BaseCommand, CommandError
from project.models import Point
from login.models import ExceptionError, SimpleLog
from login.utils import download_data
from map.utils import get_area_id
from io import StringIO
from map.models import Geodata, Geocode
from apis.models import GooglePlace, GooglePlaceCategory, GooglePlaceRequest
import json
import sys

from time import sleep
from login.models import SimpleLog, ExceptionError
#
#from https://docs.djangoproject.com/en/1.8/howto/custom-management-commands/
#

#docs: https://developers.google.com/places/documentation
#docs: https://developers.google.com/places/documentation/search?hl=es#PlaceSearchRequests
#https://maps.googleapis.com/maps/api/place/radarsearch/output?parameters


class Command(BaseCommand):
  help = 'download data from google places API for a single point_id and all google_categories'

  def add_arguments(self, parser):
    parser.add_argument('point_id', nargs=1, type=int)

  def handle(self, *args, **options):
    try:
      point_id = options['point_id'][0]
      #print(type(point_id), point_id)
      SimpleLog(category='starting management command', message='starting get_google_places, point_id=%d' %point_id).save()
      point = Point.objects.get(pk=point_id)
      #if not point.geocode:
      #  sleep(1)
      #  point = Point.objects.get(pk=point_id)
      #  if not point.geocode:
      #    SimpleLog(category='management command incomplete', message='get_google_places whit no geocode').save()
      #    sys.exit()
      print("check")
      categories = get_google_required_categories()
      for c in categories:
        url = make_url(latitude=point.latitude, longitude=point.longitude, category=c.name)
        html = download_data(url)
        io = StringIO()
        json.dump(html, io)
        GooglePlaceRequest(url=url,json=io.getvalue()).save()
        data = json.loads(html)
        places = data['results']
        update_geodata(point, c, len(places))
        update_urban_data(point, c, len(places))
        for p in places:
          save_google_place(p, c)
        sleep(1)
      SimpleLog(category='ending management command', message='ending get_google_places, point_id=%d' %point_id).save()
    except Exception as e:
      print(e)
      ee = ExceptionError(app='external command', view='get_google_places', var='{point_id:%d}' %point_id, message=str(e))
      ee.save()
  

#Save json, url and datetime data into GooglePlaceReques#
  

def save_google_place(place, category):
  google_id = place['id']
  google_place_id = place['place_id']
  latitude = place['geometry']['location']['lat']
  longitude = place['geometry']['location']['lng']
  gp = GooglePlace(latitude=latitude, longitude=longitude, google_id=google_id, google_place_id=google_place_id, googleplacecategory=category)
  gp.save()


def make_url(latitude=-33.464729, longitude=-70.598204, radius='300', category='atm'):
  key = 'AIzaSyD1lNt_uSfHEq1Q8UR9fUJPq123BouDSDQ'
  url = 'https://maps.googleapis.com/maps/api/place/radarsearch'
  url += '/json?key=' + key
  url += '&location=%s,%s' %(str(latitude), str(longitude))
  url += '&radius=%s' %str(radius)
  url += '&type=%s' %category
  return url


def update_geodata(point, category, value, url):
  lat = point.latitude
  lon = point.longitude
  area_id = get_area_id(lat, lon)
  geocode = Geocode.objects.filter(area_id=area_id)
  for g in geocode:
    if g.point_inside([lat, lon]):
      geodata = Geodata.objects.get(geocode=g.geocode)
      geodata.up_var(category.name, value)
      geodata.up_url()
      geodata.save()


def update_urban_data(point, category, value):
  point = Point.objects.get(pk=point.id)
  urban_data = {}
  try:
    urban_data = eval(point.urban_data)
  except Exception as e:
    pass
  urban_data[category.name]=value
  point.urban_data = str(urban_data)
  point.save()




def get_google_required_categories():
  gpc = GooglePlaceCategory.objects.filter(required=True)
  return gpc


