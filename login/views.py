from random import shuffle
from login.utils import validate_email
from project.models import Project, ProjectUser
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

def index(request):
  return render(request, 'login/index.html')

@login_required
def reset(request):
  return HttpResponseRedirect('/map/')

@login_required
def signout(request):
  logout(request)
  return JsonResponse({'status':'OK', 'msg':'user logged out'})

#sign in a user with a name and password
@csrf_exempt # revisar metodo de seguridad
def signin(request):
  if request.method=='POST':
    if 'email' in request.POST and 'password' in request.POST:
      email = request.POST['email'].strip()
      password = request.POST['password'].strip()
      try:
        user = User.objects.get(email=email)
      except:
        return JsonResponse({'status':'ERROR', 'msg':'invalid email'})
      user=authenticate(username=user.username, password=password)
      if not user:
        return JsonResponse({'status':'ERROR', 'msg':'wrong password'})
      if not user.is_active:
        return JsonResponse({'status':'ERROR', 'msg':'user is not active'})
      #tengo al usuario
      login(request, user)
      request.session['username']=user.username
      return JsonResponse({'status':'OK', 'msg':'user logged in'})
    else:
      return JsonResponse({'status':'ERROR', 'msg':'invalid data'})
  else:
    return JsonResponse({'status':'ERROR', 'msg':'invalid http method'})


#View of terms and conditions.
def terms(request):
  return render(request, 'login/terms.html')


@csrf_protect
@login_required
def user(request):
  try:
    username = request.session['username']
    user = User.objects.get(username=username)
  except:
    return JsonResponse({'status':'ERROR', 'msg':'unknoun user'})
  #tengo al usuario
  if request.method=='GET':
    ret = {}
    #ret['id'] = user.id
    ret['first_name'] = user.firstname
    ret['last_name'] = user.last_name
    ret['email'] = user.email
    ret['status'] = 'OK'
    ret['msg'] = ''
    return JsonResponse(ret)

  elif request.method=='PUT':
    updated = False
    if 'first_name' in request.POST:
      user.first_name = request.POST['first_name'].strip()
      updated = True
    if 'last_name' in request.POST:
      user.last_name = request.POST['last_name'].strip()
      updated = True
    if 'new_password' in request.POST:
      if 'password' in request.POST:
        new_password = request.POST['new_password'].strip()
        password = request.POST['password'].strip()
        if user.check_password(password):
          user.set_password(new_password)
          updated = True
        else:
          return JsonResponse({'status':'ERROR', 'msg':'invalid current password'})
      else:
        return JsonResponse({'status':'ERROR', 'msg':'no current password'})

    if updated:
      user.save()
      return JsonResponse({'status':'OK', 'msg':'user updated'})
    else:
      return JsonResponse({'status':'OK', 'msg':'user not updated'})

    return JsonResponse({'status':'ERROR', 'msg':'test function'})
  elif request.method=='DELETE':
    user.is_active=False
    user.save()
    return JsonResponse({'status':'OK', 'msg':'user deleted'})
  else:
    return JsonResponse({'status':'ERROR', 'msg':'invalid http method'})

@csrf_exempt
def useradd(request):
  if request.method=='POST':
    try:
      first_name = request.POST['first_name'].strip()
      last_name = request.POST['last_name'].strip()
      email = request.POST['email'].strip()
      password = request.POST['password'].strip()
      terms = request.POST['terms'].strip()
      print(first_name)
      print(last_name)
      print(email)
      print(password)
      print(type(terms), terms)
    except:
      return JsonResponse({'status':'ERROR', 'msg':'invalid data'})
    if not first_name or not last_name or not email or not password or not terms:
      return JsonResponse({'status':'ERROR', 'msg':'incomplete data'})
    if not validate_email(email):
      return JsonResponse({'status':'ERROR', 'msg':'invalid email'})
    if terms != 'true':
      return JsonResponse({'status':'ERROR', 'msg':'terms not accepted'})
    exits = User.objects.filter(email=email)
    if exits:
      return JsonResponse({'status':'ERROR', 'msg':'user already exist'})
    #paso todos los filtros
    new_username = aux_keygen()
    user = User.objects.create_user(username=new_username, password=password, first_name=first_name, last_name=last_name, email=email)
    user.save()
    user=authenticate(username=new_username, password=password)
    p = Project(name="Initial Project")
    p.save()
    pu = ProjectUser(project=p, user=user, permission=0)
    pu.save()
    login(request, user)
    request.session['username']=user.username
    return JsonResponse({'status':'OK', 'msg':'added user'})
  else:
    return JsonResponse({'status':'ERROR', 'msg':'invalid http method'})

#curl -H "Content-Type: application/json" -X POST -d '{"email":"hola","password":"xyz", "repass":"xyz"}' http://localhost:8000/login/user
#

#curl --data "email=hola@hola.com&password=val" http://localhost:8000/login/user/
#curl --data "first_name=larry&last_name=gonzalez&email=larry@hit-map.com&password=pass" http://localhost:8000/login/user/

def aux_keygen(l=30):
  lletters = 'abcdefghijklmnopqrstuvwxyz'
  uletters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  numbers = '0123456789'
  data = list(lletters + uletters + numbers)
  shuffle(data)
  return(''.join(data[:l]))

def keygen():
  key = aux_keygen()
  users = User.objects.filter(username=key)
  if users:
    return keygen()
  return key

