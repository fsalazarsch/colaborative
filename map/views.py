from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.http import JsonResponse
from django.core.exceptions import MultipleObjectsReturned

from map.models import Point, Geodata, UrbanDataDescription
from project.models import Project, ProjectUser, HitscoreModel, HitscoreValue, Reports
from map.models import Geodata
from django.contrib.auth.models import User

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, inch
import io
from datetime import datetime
import time
from urllib.request import urlopen
from PIL import Image
from login.utils import now
#from login.models import CustomeUser
from map.utils import get_google_map_image


@login_required
def index(request):
  context = {}
  context.update(csrf(request))
  username = request.session['username']
  user = User.objects.get(username=username)
  if user.is_superuser:
    proj = Project.objects.all()
    proj = [[p.id, p.name] for p in proj]
  else:
    proj_user = ProjectUser.objects.filter(user=user)
    proj_user = [p.project_id for p in proj_user]
    proj = Project.objects.filter(pk__in=proj_user)
    proj = [[p.id, p.name] for p in proj]
  context['username'] = user.email
  context['c_projects'] = proj
  context['username'] = user.email
  return render(request, 'map/index.html', context)


def temp(request):
  return render_to_response('map/temp.html')


@login_required
def get_point_scoreboard(request):
  #faltan casos de errores y de otro usuario
  username = request.session['username']
  point_id = request.GET['point_id']

  user = User.objects.get(username=username)
  point = Point.objects.get(pk=point_id)
  project = point.project  

  try:
    hm = project.hitscoremodel
    variables = eval(hm.attributes)
  except Exception as e:
    variables = ['adt_101', 'poi_101', 'den_101', 'deg_101', 'beh_101'] #default variables
  print(variables)
  try:
    point_vars = Geodata.objects.get(geocode=point.geocode).get_vars()
  except Exception as e:
    point_vars = {}
 
  ret = [point.get_readable_status(), point.get_hitscore_or_salesindex()]
  ret += [point.created_by, point.opening_date, point.modified_by, point.last_update]
  for v in variables:
    print(v)
    if v in point_vars:
      ret.append(v)
    else:
      ret.append(None)
  return JsonResponse(ret, safe=False)



@login_required
def score_board(request): # A revisar
  username = request.session['username']
  user = User.objects.get(username=username)
  context = {}
  try:
    project_id = int(request.GET['project_id'])
    project = Project.objects.get(pk=project_id)
    points = project.point_set.order_by('-id');
  except Exception as e:
    print(e)
    context['response'] = 'error'
    context['error_message'] = 'You cannot read this project\'s points'
    return render(request, 'map/score_board.html', context)

  try:
    hitscoremodel = HitscoreModel.objects.get(project=project, valid=True)
    variables = eval(hitscoremodel.attributes)
  except Exception as e:
    variables = ['adt_101', 'poi_101', 'den_101', 'deg_101', 'beh_101']
  if len(variables) != 5:
    variables = ['adt_101', 'poi_101', 'den_101', 'deg_101', 'beh_101']

  points_data = []
  for point in points:
    point_data = {}
    try:
      point_vars = Geodata.objects.get(geocode=point.geocode).get_vars()
    except Exception as e:
      point_vars = {}
    for variable in variables:
      if variable in point_vars:
        point_data[variable] = int(point_vars[variable])
    point_data['id'] = point.id
    point_data['lat'] = point.latitude
    point_data['lng'] = point.longitude
    point_data['status'] = point.status
    point_data['status_readable'] = point.get_readable_status()
    point_data['edition_date'] = point.edition_date
    point_data['edited_by'] = point.edited_by

    point_data['hitscore'] = point.get_hitscore_or_salesindex()
    if not point_data['hitscore']:
      point_data['hitscore'] = ''

    point_data['location_name'] = point.get_var('location_name')
    if not point_data['location_name']:
      point_data['location_name'] = ''

    points_data.append(point_data)

  context['points_data'] = points_data
  context['response'] = 'OK'
  context['variables'] = variables

  vardesc = []# [[name,desc]]
  for v in variables:
    udd = None
    try:
      udd = UrbanDataDescription.objects.get(code=v)
    except Exception as e:
      pass
    aux = []
    if udd:
      aux.append(udd.name if udd.name else v)
      aux.append(udd.description if udd.description else v)
    else:
      aux = [v,v]
    vardesc.append(aux)
  context['vardesc'] = vardesc
  print(vardesc)
  return render(request, 'map/score_board.html', context)



