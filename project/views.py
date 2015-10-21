from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from map.models import Geocode, Geodata
from .models import Point, Project, ProjectUser
from django.contrib.auth.models import User
from django.http import JsonResponse
from project.models import HitscoreModel, HitscoreValue
from math import exp, log
from .forms import ProjectForm
from django.db.models import Q
from login.models import SimpleLog, ExceptionError
from login.utils import now
from project.reportes import Reporte_Location_Summary, Reporte_Scoreboard
import datetime
import time
import os

# Create your views here.
@login_required
def create_project(request):
  username = request.session['username']
  user = User.objects.get(username=username)
  new_project_name = request.POST['new_project']
  #check if there is an old project with that name
  old_projects = ProjectUser.objects.filter(user__username=username, project__name=new_project_name)
  if old_projects.count() > 0:
    #A project with that name already exists. Return id=-1
    return JsonResponse({'project_name':"",'project_id': -1})
  else:
    #there is no old project with that name. Create one, save it and return its id.
    proj = Project(name=new_project_name)
    proj.save()
    proj_user = ProjectUser(user=user, project=proj)
    proj_user.save()
    return JsonResponse({'project_name':proj.name, 'project_id':proj.id})

###################
# POINT FUNCTIONS #
###################

@login_required
def add_point(request):
  aux = csrf(request)
  username = request.session['username']
  proj = request.POST['project']
  lat = request.POST['lat']
  lon = request.POST['lon']
  user = User.objects.get(username=username)
  proj = Project.objects.get(pk=proj)
  if user.is_superuser:
    new_point = Point(project=proj, latitude=lat, longitude=lon, created_by=user, edited_by=user, status=6)
  else:
    new_point = Point(project=proj, latitude=lat, longitude=lon, created_by=user, edited_by=user)
  new_point.save()
  os.system("python3.4 manage.py recover_geocode %s" %str(new_point.id))
  os.system("python3.4 manage.py get_google_places %s &" %str(new_point.id))
  return JsonResponse({'response':'OK','id':new_point.id, 'status':new_point.status})




@login_required
def update_point_sales(request):
  try:
    username = request.session['username']
    point_id = request.POST['point_id']

    user = User.objects.get(username=username)
    point = Point.objects.get(pk = point_id)
    updated = False
  except Exception as e:
    print(e)
    return JsonResponse({'msg': 'some error occurs','exception_message':str(e) }) 
    

  yearly_sales = request.POST['yearly_sales'].strip()
  if yearly_sales:
    try:
      yearly_sales = int(yearly_sales)
    except Exception as e:
      print(e)
      return JsonResponse({'msg': 'sales must be numeric','exception_message':str(e) }) 
    point.sales = yearly_sales
    updated = True

  opening_date = request.POST['date_opening'].strip()
  if opening_date: #viene como "YYYY-MM-DD"
    try:
      point.opening_date = opening_date
      updated = True
    except Exception as e:
      print(e)
      return JsonResponse({'msg': 'date of opening error','exception_message':str(e) }) 

  opened_days = request.POST['days_opened'].strip()
  if opened_days:
    try:
      opened_days = int(opened_days)
    except Exception as e:
      print(e)
      return JsonResponse({'msg': 'days opened must be numeric','exception_message':str(e) })
    point.opened_days = opened_days
    updated = True

  square_feet = request.POST['square_feet'].strip()
  if square_feet:
    try:
      square_feet = int(square_feet)
    except Exception as e:
      print(e)
      return JsonResponse({'msg': 'square feet must be numeric','exception_message':str(e) })
    point.square_feet = square_feet
    updated = True

  if updated:
    point.edition_date = now()
    point.edited_by = user
    point.save()
    point.project.updated = True
    point.project.save()
    update_sales_index(point.project_id)

  return JsonResponse({'msg': 'Done'})



@login_required
def update_point_notes(request):
  try:
    username = request.session['username']
    point_id = request.POST['point_id']

    user = User.objects.get(username=username)
    point = Point.objects.get(pk = point_id)
  except Exception as e:
    print(e)
    return JsonResponse({'msg': 'some error occurs','exception_message':str(e) }) 

  def aux_update(key, value):
    if value:
      point.up_var(key,value)
  try:
    aux_update('owner', request.POST['notes_owner'].strip())
    aux_update('contact', request.POST['notes_contact'].strip())
    aux_update('address', request.POST['notes_address'].strip())
    aux_update('tip_price', request.POST['notes_tip_price'].strip())
    aux_update('tip_area', request.POST['notes_tip_area'].strip())
    aux_update('price', request.POST['notes_price'].strip())
    aux_update('area', request.POST['notes_area'].strip())
  except Exception as e:
    print(e)
  return JsonResponse({'msg': 'Done'})




def update_sales_index(project_id):
  project = Project.objects.get(pk=project_id)
  points = Point.objects.filter(project=project).exclude(sales__isnull=True)
  #sales_index updated
  sales = [float(p.sales) for p in points]
  mf = 100/(sum(sales)/len(sales))
  sales_index = list(map(lambda x: x*mf, sales))
  for i in range(len(points)):
    points[i].sales_index = sales_index[i]
    points[i].save()


@login_required
def get_point_sales(request):
  try:
    point_id = request.POST['point_id']
    point = Point.objects.get(pk = point_id)
    sales = {}
    notes = {} #agregado
   
    if point.sales:
      sales['sales'] = point.sales
    if point.opening_date:
      cadena=str(point.opening_date)
      #position=cadena.find('T')
      aux1=cadena[0:10]
     # aux = datetime.date(aux1[0:4],aux1[6:7],aux1[9:10])
      #aux=aux2.format("%d-%m-%Y")

      #sales['opening_date'] = ":%d/%m/%Y".format(point.opening_date)
      #sales['opening_date'] =datetime.date(point.opening_date)
      #sales['opening_date'] = point.opening_date#.format("%d/%m/%Y")
      sales['opening_date'] =  aux1
    if point.square_feet:
      sales['square_feet'] = point.square_feet
    if point.opened_days:
      sales['opened_days'] = point.opened_days
    if point.var:
      notes = eval(point.var)

    return JsonResponse({'sales':sales,'notes':notes})
  except Exception as e:
    return JsonResponse({'msg':'error'})

@login_required
def get_points(request):
  username = request.session['username']
  proj_id = request.POST['p_proj_id']
  all_points = Point.objects.filter(project=proj_id)
  all_points = [[p.latitude, p.longitude, p.id, p.status, p.get_hitscore_or_salesindex()] for p in all_points]
  return JsonResponse({'points':all_points})

@login_required
def get_points_information(request):
  username = request.session['username']
  id_point = request.POST['point_id']
  point = Point.object.get(pk=id_point)
  return JsonResponse({'point_information':point.var})

@login_required
def get_point_data(request):
  try:
    point_id = request.POST['point_id']
    point = Point.objects.get(id = point_id)
    point_vars = point.get_vars()
    if point_vars:
      point_vars['id'] = point.id
    else:
      point_vars = { 'id': point.id }
    point_vars['status'] = point.status
    point_vars['sales'] = point.sales
    point_vars['response'] = 'OK'
    return JsonResponse( point_vars )
  except BaseException as e:
    return JsonResponse({ 'response':'error', 'error_message': str(e) })

@login_required
def get_hitscore(request):
  try:
    point_id = request.POST['point_id']
    point = Point.objects.get(pk=point_id)
  except Exception as e:
    print("wrong point_id")
    return JsonResponse({})
  ret = point.hitscore()
  if ret:
    return JsonResponse({'hitscore':ret})
  return JsonResponse({})


@login_required
def predict_hitscore(request):
  try:
    point_id = request.POST['point_id']
    point = Point.objects.get(pk=point_id)
    hitscoremodel = HitscoreModel.objects.get(project=point.project, valid=True)
  except Exception as e:
    print("no point or no model")
    return JsonResponse({})
  os.system("python3.4 manage.py compute_hitscore %d %d" %(hitscoremodel.id, point.id))
  return get_hitscore(request)



@login_required
def delete_point(request):
  aux = csrf(request)
  point_id = request.POST['point_id']
  point = Point.objects.get(pk=point_id)
  point.delete()
  return JsonResponse({'msg':'done'})





@login_required
def info_tabla(request):  # funcion para el scoreboard
  username = request.session['username']
  id_proyecto = request.POST['p_proj_id']
  modelo = HitscoreModel.objects.filter(project=id_proyecto)
  modelo  = [[p.valid] for p in modelo]
  return JsonResponse({'valor':'ok'})






@login_required
def edit_project(request, project_id):
  user = request.session['username']
  user = User.objects.get(username=user)
  project = get_object_or_404(Project, pk=project_id)
  context = {'project_id': project_id}
  #verify this user can access this project
  try:
    project_user = ProjectUser.objects.get(user=user, project=project,  permission__lte= 1) #permission__lte=1 means: owner or write access
  except ProjectUser.DoesNotExist:
    #this user cannot modify this project
    context['response'] = 'error'
    context['error_message'] = 'You cannot edit this project.'
    return render(request, 'project/index.html', context)
  #this user can modify this project
  project_owner = ProjectUser.objects.get(Q(project=project), Q(permission = 0))
  context['project_owner'] = project_owner.user
  
  project_users = ProjectUser.objects.filter(Q(project=project),~Q(permission = 0))
  context['project_users'] = project_users
  context['response'] = 'OK'
  if request.method == 'GET':
    project_form = ProjectForm({'project_name':project.name})
    context['form'] = project_form
  elif request.method == 'POST':
    project_form = ProjectForm(request.POST)
    if project_form.is_valid():
      project.name = project_form.cleaned_data['project_name']
      project.save()
      return HttpResponseRedirect('/map/')
    else:
      context['form'] = project_form
  return render(request, 'project/index.html',context)




@login_required
def projectuser_set_permissions(request):
  username = request.session['username']
  user = get_object_or_404(User, username=username)
  user_id = user.id
  new_permissions = request.POST['new_permissions']
  project_id = request.POST['project_id']
  user_to_set_id = request.POST['user_to_set_id']
  response = {}
  #verify this user can access this project
  try:
    project_user = ProjectUser.objects.get(user=user.id, project=project_id, permission__lte= 1) #permission__lte=1 means: owner or write access
  except ProjectUser.DoesNotExist:
    #this user cannot modify this project
    response['response'] = 'error'
    response['error_message'] = 'You cannot edit this project.'
    return JsonResponse(response)
  #verify if user_to_set is in this project
  try:
    projectuser_to_set = ProjectUser.objects.get(user=user_to_set_id, project=project_id)
  except ProjectUser.DoesNotExist:
    #user_to_set is not in this project
    response['response'] = 'error'
    response['error_message'] = 'User is not in the project'
    return JsonResponse(response)
   #if user_to_set is owner, we cannot set his/her permissions
  if projectuser_to_set.permission == 0:
    response['response'] = 'error'
    response['error_message'] = 'You cannot set owner\'s permissions'
    return JsonResponse(response)
  #verify new_permissions is correct
  if new_permissions != '1' and new_permissions != '2':
    response['response'] = 'error'
    response['error_message'] = 'Incorrect permissions type'
    return JsonResponse(response)
  #set his/her permissions
  projectuser_to_set.permission = new_permissions
  projectuser_to_set.save()
  response['response'] = 'OK'
  return JsonResponse(response)



@login_required
def add_user(request):
  print("call to add_user")
  username = request.session['username']
  user = User.objects.get(username=username)
  project_id = request.POST['project_id']
  project = Project.objects.get(pk=project_id)
  new_user_mail = request.POST['new_user_mail']
  print(new_user_mail)
  response = {}
  try:
    project_user = ProjectUser.objects.get(user=user, project=project, permission=0) #permission=0 means: owner only
  except ProjectUser.DoesNotExist:
    #this user cannot modify this project
    response['response'] = 'error'
    response['error_message'] = 'Only the owner may add a new user'
    return JsonResponse(response)
  #get the new user of the project
  try:
    new_user = User.objects.get(email=new_user_mail)
  except User.DoesNotExist:
    #there is no user with that mail
    response['response'] = 'error'
    response['error_message'] = 'There is no user with that e-mail'
    return JsonResponse(response)
  #verify if this new user is not in the project already
  try:
    old_projectuser = ProjectUser.objects.get(user=new_user, project=project)
    response['response'] = 'error'
    response['error_message'] = 'That user is already in the project'
    return JsonResponse(response)
  except ProjectUser.DoesNotExist:
    pass
  new_projectuser = ProjectUser(user=new_user, project=project, permission=2)
  new_projectuser.save();
  response['response'] = 'OK'
  response['project_user_id'] = new_projectuser.id
  response['project_id'] = new_projectuser.project.id
  response['user_id'] = new_projectuser.user.id
  response['user_mail'] = new_projectuser.user.email
  return JsonResponse(response)


@login_required
def delete_user(request):
  username = request.session['username']
  project_user_id = request.POST['project_user_id']
  user = get_object_or_404(User, username=username)
  response = {}
  #verify there is projectuset
  try:
    projectuser_to_del = ProjectUser.objects.get(pk=project_user_id)
  except ProjectUser.DoesNotExist:
    #there are no user to del
    response['response'] = 'error'
    response['error_message'] = 'User to delete where not finded'
    return JsonResponse(response)
  #verify this user can add a new user
  try:
    project_id = projectuser_to_del.project.id
    project_user = ProjectUser.objects.get(user=user.id, project=project_id, permission=0) #permission=0 means: owner only
  except ProjectUser.DoesNotExist:
    #this user cannot modify this project
    response['response'] = 'error'
    response['error_message'] = 'Only the owner may delete a user'
    return JsonResponse(response)
  #verify user_to_del is not the owner
  if projectuser_to_del.permission == 0:
    response['response'] = 'error'
    response['error_message'] = 'Project owner cannot be deleted'
    return JsonResponse(response)
  #proceed eliminate projectuser
  projectuser_to_del.delete()
  response['response'] = ['OK']
  return JsonResponse(response)

@login_required
def change_point_status(request):
  username = request.session['username']
  point_id = request.POST['marker_id']
  status = request.POST['status']
  user = get_object_or_404(User, username=username)
  point = get_object_or_404(Point, pk=point_id)
  response = {}
  #verify this point is in a project with write permissions to this user
  try:
    projectuser = ProjectUser.objects.get(user=user, project__point__in=[ point ], permission__lte= 1)
  except ProjectUser.DoesNotExist:
    response['response'] = 'error'
    response['error_message'] = 'You cannot write in this project'
    return JsonResponse(response)
  #verify status
  try:
    status = int(status)
  except ValueError:
    response['response'] = 'error'
    response['error_message'] = 'Wrong status format'
    return JsonResponse(response)
  if status < 1 or status > 5:
    response['response'] = 'error'
    response['error_message'] = 'Wrong status'
    return JsonResponse(response)
  point.status = status
  point.save()
  response['response'] = 'OK'
  response['status'] = point.status
  response['id'] = point.id
  return JsonResponse(response)



######################
# HITSCORE FUNCTIONS #
######################
@login_required
def make_hitscore_model(request):
  project_id = int(request.POST['project_id'].strip())
  print(project_id, type(project_id))
  if project_id < 0:
    return JsonResponse({'msg':'OK'})
  launching = 'python3.4 manage.py make_hitscore_model %s &' %str(project_id)
  os.system(launching)
  sl = SimpleLog(category='launch management command', message=launching)
  sl.save()
  return JsonResponse({'msg':'OK'})


@login_required
def project_model_message(request):
  project_id = request.POST['project_id']
  project = Project.objects.get(pk=project_id)
  return JsonResponse({'msg':project.model_msg})



@login_required
def set_location_name(request):
  point_id = request.POST['point_id']
  location_name = request.POST['location_name']
  username = request.session['username']
  response = {}
  try:
    point = Point.objects.get(id=point_id)
    point_vars = point.up_var('location_name', location_name)
    project_user = ProjectUser.objects.get(user__username=username, project__point__in=[ point ], permission__lte= 1) # permission__lte=1 means write permissions
    response['response'] = 'OK'
    response['location_name'] = location_name
  except Point.DoesNotExist:
    response['response'] = 'error'
    response['error_message'] = 'Point not found'
  except ProjectUser.DoesNotExist:
    response['response'] = 'error'
    response['error_message'] = 'You can\'t modify this project.'
  return JsonResponse(response)

@login_required
def get_point_report(request):
  response = {}
  try:
    point_id = request.POST['point_id']
    username = request.session['username']
    report_url = Reporte_Location_Summary(point_id, username)
    response['response'] = 'OK'
    response['report_url'] = report_url
    response['point_id'] = point_id
  except KeyError:
    response['response'] = 'error'
    response['error_message'] = 'No point where given'
    #except BaseException as e:
    #response['response'] = 'error'
    #response['error_message'] = str(e)
  return JsonResponse(response)

@login_required
def get_project_report(request):
  response = {}
  try:
    project_id = request.POST['project_id']
    username = request.session['username']
    report_url = Reporte_Scoreboard(project_id, username)
    response['response'] = 'OK'
    response['report_url'] = report_url
    response['project_id'] = project_id
  except KeyError:
    response['response'] = 'error'
    response['error_message'] = 'No project where given'
  except BaseException as e:
    response['response'] = 'error'
    response['error_message'] = str(e)
  return JsonResponse(response)


@login_required
def delete_project(request):
  username = request.session['username']
  user = User.objects.get(username=username)
  response = {}
  try:
    project_id = request.POST['project_id']
    projectuser = ProjectUser.objects.get(user=user, project=project_id, permission=0) #permission=0 means project owner
    project = projectuser.project
    project.delete()
    response['response'] = 'OK'
  except ProjectUser.DoesNotExist:
    response['response'] = 'error'
    response['error_message'] = 'Only the owner may delete a project'
  except KeyError:
    response['response'] = 'error'
    response['error_message'] = 'no project_id were given'
  except BaseException as e:
    response['response'] = 'error'
    response['error_message'] = str(e)
  return JsonResponse(response)

@login_required
def project(request):
  try:
    username = request.session['username']
    user = User.objects.get(username=username)
  except:
    return JsonResponse({'status':'ERROR', 'msg':'not logged in'})
  if request.method=='POST':
    try:
      project_name = request.POST['project_name']
    except:
      return JsonResponse({'status':'ERROR', 'msg':'no project_name'})
    if not project_name:
      return JsonResponse({'status':'ERROR', 'msg':'no project_name'})
    p = Project(name="Initial Project")
    p.save()
    pu = ProjectUser(project=p, user=user, permission=0)
    pu.save()
    return JsonResponse({'status':'OK', 'msg':'project_added', 'project_id':p.id})
  elif request.method=='GET':
    pass
  elif request.method=='PUT':
    pass
  elif request.method=='DELETE':
    pass
  else:
    return JsonResponse({'status':'ERROR', 'msg':'invalid http method'})
