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
import time
from urllib.request import urlopen
from PIL import Image
from login.utils import now
from map.utils import get_google_map_image
from django.conf import settings



def get_showable_attributes(project_id, geocode):
  ret = []
  try:
    hitmod = HitscoreModel.objects.get(project_id=project.id)
    ret = eval(hitmod.attributes)
  except Exception as e:
    pass
  if len(ret) != 5:
    if str(geocode)[0]=='1':
      ret = ['adt_101', 'poi_101', 'den_101', 'deg_101', 'beh_101']
    if str(geocode)[0]=='2':
      ret = ['adt_201', 'poi_201', 'den_201', 'deg_201', 'beh_201']
  return ret




def Reporte_Location_Summary(point_id, s_user):
  print("starting point report")
  fecha = now()
  point = Point.objects.get(id = point_id)
  project = point.project
  status = point.status
  status = 'status_%d.svg' %status
  # saca email del objeto User
  email_user = User.objects.get(username=s_user)
  report_image = get_google_map_image(point.latitude, point.longitude, status)
  diccio = point.get_vars()

  print("location report check 1")

  area = ''
  location = ''
  if diccio:
    if 'location_name' in diccio:
      location = diccio['location_name']
    if 'area' in diccio:
      area = diccio['area']
  hitscore = 'no hitscore computed'
  if point.hitscore():  # hitscore se saca de una funcion del modelo
    hit = point.hitscore()
    hitscore = int(hit)

  print("location report check 2")

  file_url = settings.STATIC_ROOT +'report/'+point_id + "_" + fecha + ".pdf"
  url = settings.STATIC_URL+'report/'+point_id + "_" + fecha + ".pdf"
  print(file_url)
  print(url)
  num_correlativo = Reports(url_report=file_url)
  num_correlativo.save()

  #saca geocode del point
  geocode = point.geocode



  # saca nombre de las variables de hitscoremodel
  list_names = get_showable_attributes(project.id, geocode)
  print("location report check 3")

  # diccionario con valores de las variables
  geodata = Geodata.objects.get(geocode=geocode)
  variables = eval(geodata.var)
  c = canvas.Canvas(file_url)
  c.setFont("Helvetica", 20)
  # ancho - alto
  c.setStrokeColorRGB(0,0,0)
  c.rect(3.51*cm,8.44*cm,14.16*cm,11.68*cm, fill=1) # cuadrado de marco de la f$
  #derecha - arriba - agranda/achica horizontal - agranda/achica vertical
  c.setFillColorRGB(0,0,0)
  c.drawString(7*cm, 26.4*cm, "LOCATION REPORT")
  c.setFont("Helvetica", 10)
  c.drawString(3.5*cm, 26.2*cm, "_________________________________________________________________________")

  print("location report check 4")
  print(fecha)
  print(project.name)

  c.setFont("Helvetica", 10)
  c.drawString(3.5*cm, 25.2*cm, "Date of Evaluation: "+fecha)
  c.drawString(3.5*cm, 24.8*cm, "Project: " + project.name)
  c.drawString(3.5*cm, 24.4*cm, "User: " + email_user.email)
  c.drawString(3.5*cm, 23.7*cm, "Notes: no notes added")
  c.setFont("Helvetica", 30)

  c.setFillColorRGB(0.90,0.90,0.90)
  c.setStrokeColorRGB(255,255,255)
  c.rect(3.50*cm,20.6*cm,14.2*cm,2*cm, fill=1)
  #derecha - arriba - agranda/achica horizontal - agranda/achica vertical

  c.setFillColorRGB(0,0,0)
  c.drawString(3.7*cm, 21.4*cm, "HITSCORE: ")

  if(hitscore == 'no hitscore computed'):
    c.setFont("Helvetica", 12)
  else:
   c.setFont("Helvetica", 30)
  print("location report check 5")
  c.drawString(9.7*cm, 21.4*cm, str(hitscore) + " *")

  c.setFont("Helvetica", 10)
  c.drawString(3.7*cm, 20.9*cm, "*Scoring according to type and location")

  textobject = c.beginText()
  textobject.setTextOrigin(14.9*cm, 22*cm)
  textobject.setFont("Helvetica", 8)
  textobject.textLines('''Hitscore is a sales
  prediction index:
  100 is the current
  average sales''')
  c.drawText(textobject)
  num = Reports.objects.get(url_report=file_url)
  c.setFont("Helvetica", 12)
  c.drawString(3.5*cm, 28.3*cm, "Certified: N° " + str(num.id))

  c.setFont("Helvetica", 11)
  c.drawImage(report_image, 100, 240, width=400, height=330)

  c.setFillColorRGB(0.90,0.90,0.90)
  c.rect(3.45*cm,3.3*cm,14.3*cm,4.4*cm, fill=1)
  #derecha - arriba - agranda/achica horizontal - agranda/achica vertical
  
  c.setFillColorRGB(0,0,0)
  c.drawString(3.7*cm, 7.1*cm, "SELECTED VARIABLES")
  c.setFont("Helvetica", 10)
  print("location report check 6")
  num = len(list_names)
  espacio = 0
  nombre = ''

  for at in list_names:
    val = -1
    if at in variables:
      val = variables[at]
    try:
      name = UrbanDataDescription.objects.get(code=at).description
    except Exception as e:
      name = at

    if(len(name) > 70):
      for letra in name:
        if(len(nombre) < 70):
          nombre = nombre + letra
    else:
      nombre = name

    c.drawString(3.7*cm, (6.1-espacio)*cm, nombre + ": ")
    c.drawString(15*cm, (6.1-espacio)*cm, str('{:,}'.format(val)))
    nombre = ''
    espacio = espacio + 0.5
  print("location report check 7")

  c.setFont("Helvetica-Bold", 10)
  c.drawString(3.5*cm, 1.9*cm, "_________________________________________________________________________ ")
  c.setFont("Helvetica", 10)
  c.drawString(3.5*cm, ((1.8+espacio)-3)*cm, "www.hit-map.com | info@hit-map.com  | +562 586 50 60 | Huérfanos 862, of. 612, Santiago")
  ruta_logo = "map/static/map/Logotipo_Hitmap.png"
  c.drawImage(ruta_logo, 405, 780, width=100, height=40, mask='auto')

  c.showPage()

  ruta_logo = "map/static/map/Logotipo_Hitmap.png"
  c.drawImage(ruta_logo, 405, 780, width=100, height=40, mask='auto')

  num = Reports.objects.get(url_report=file_url)
  c.setFont("Helvetica", 12)
  c.drawString(3.5*cm, 28.3*cm, "Certified: N° " + str(num.id))

  c.drawString(3.5*cm, 22.5*cm, "Definitions")

  seg_pag = c.beginText()
  seg_pag.setTextOrigin(3.5*cm, 21.5*cm)
  seg_pag.setFont("Helvetica", 10)
  seg_pag.textLines(''' Hitscore is a statistical projection index, based on current average sales of open stores (100).
  This means that if a Histcore is 120 that  location, according to a statistical profile, could
  sell 20% over average. The hitscore is meant to easily inform decision-makers by synthetizing
  hundreds of variables in one indicator. For  more information, info@hit-map.com.
  ''')
  c.drawText(seg_pag)

  c.setFont("Helvetica", 12)
  c.drawString(3.5*cm, 18*cm, "Metodology")

  seg_pag2 = c.beginText()
  seg_pag2.setTextOrigin(3.5*cm, 17*cm)
  seg_pag2.setFont("Helvetica", 10)
  seg_pag2.textLines('''Hitmap algorythm values more tha 180 urban variables from multiple certified sources, and use
  them all to understand how the urban enviroment is explaining current sales (more details at
  www.hit-map.com). With this information, Hitmap can do a statistical projection of sale on
  new locations where data is available.
  ''')

  c.drawText(seg_pag2)
  print("location report check 8")
  
  c.setFont("Helvetica", 12)
  c.drawString(3.5*cm, 13.5*cm, "Certification")

  seg_pag3 = c.beginText()
  seg_pag3.setTextOrigin(3.5*cm, 12.5*cm)
  seg_pag3.setFont("Helvetica", 10)
  print("location report check 9")

  seg_pag3.textLines('''The certification number at the top left of the Location Report, is a control system though wich
  you validate this is a true document. To do this, you have to enter www.hit-map.com or right
  to info@hit-map.com.
  ''')
  c.drawText(seg_pag3)
  c.setFont("Helvetica-Bold", 10)
  c.drawString(3.5*cm, 1.9*cm, "_________________________________________________________________________ ")
  c.setFont("Helvetica", 10)
  print("location report check 10")

  c.drawString(3.5*cm, ((1.8+espacio)-3)*cm, "www.hit-map.com | info@hit-map.com  | +562 586 50 60 | Huérfanos 862, of. 612, Santiago")
  print("location report check 10")

  c.save()
  return url





def Reporte_Scoreboard(project_id, s_user):
  print("starting project report")
  fecha = now()
  project = Project.objects.get(pk=project_id)
  email_user = User.objects.get(username=s_user)
  # objeto point que contiene las variables location name y hitscore
  points = Point.objects.filter(project=project).exclude(geocode__isnull=True)
  points = [[p.id, p.var, p.geocode, p.status] for p in points]

  geocode = points[0][2]
  list_names = get_showable_attributes(project.id, geocode)

  file_url = settings.STATIC_ROOT+'scoreboard_'+ project_id + fecha+".pdf"
  url = settings.STATIC_URL+'scoreboard_'+ project_id + fecha+".pdf"

  num_correlativo = Reports(url_report=file_url)
  num_correlativo.save()
  c = canvas.Canvas(file_url,landscape(A4))

  num = Reports.objects.get(url_report=file_url)
  c.setFont("Helvetica", 12)
  c.drawString(3.5*cm, 19.5*cm, "Certified: N° " + str(num.id))

  c.setFillColorRGB(0.90,0.90,0.90)
  c.setStrokeColorRGB(0.90,0.90,0.90)
  c.rect(8.25*cm,12.7*cm,2*cm,1.3*cm, fill=1) # original
  #der/izq - up/down - agranda/achica horizontal - agranda/achica vertical
  c.setFillColorRGB(0,0,0)
  ruta_logo = "map/static/map/Logotipo_Hitmap.png"
  c.drawImage(ruta_logo, 640, 540, width=100, height=40, mask='auto')

  c.setFont("Helvetica", 20)
  c.drawString(11*cm , 17*cm,"PROJECT REPORT")
  c.setFont("Helvetica-Bold", 10)
  c.drawString(3.5*cm , 16.8*cm, "_______________________________________________________________________________________________________________")
  c.setFont("Helvetica", 10)
  c.drawString(3.5*cm, 16*cm, "Date: "+fecha)
  c.drawString(3.5*cm, 15.6*cm, "Project: "+project.name)
  c.drawString(3.5*cm, 15.2*cm, "User: "+email_user.email)
  c.setFont("Helvetica-Bold", 10)
  c.drawString(3.5*cm , 14*cm, "_______________________________________________________________________________________________________________")
  espacio = 0
  c.drawString(3.5*cm, 13.4*cm, "Location Name")
  esp2 = 0  # variable de espacio vertical para mostrar los datos
  nombre_var = ''

  # comienzo del for
  for i in range(len(list_names)):
    name = UrbanDataDescription.objects.get(code=list_names[i])

    if(len(name.name) > 13):
      for letra in name.name:
        if(len(nombre_var) < 13):
          nombre_var = nombre_var + letra
    else:
      nombre_var = name.name

    c.drawCentredString((13.7+espacio)*cm, 13.4*cm, nombre_var)
    nombre_var = ''
    espacio = espacio + 2.5

  c.drawString(8.5*cm, 13.4*cm, "Hitscore")
  c.drawString(11*cm, 13.4*cm, "Status")

  c.drawString(3.5*cm , 13.2*cm, "_______________________________________________________________________________________________________________")
  nombre_final = ''
  status = ''
  # ciclo que recupera los geocodes de los puntos del proyecto
  for w in range(len(points)):
    # diccionario con valores de las variables
    geodata = Geodata.objects.get(geocode=points[w][2])
    variables = eval(geodata.var)
    esp = 0 # variable para espacio horizontal

    # ciclo que recupera los valores de las variables de todos los puntos del proyecto
    for e in range(len(list_names)):
      c.setFillColorRGB(0.90,0.90,0.90)
      c.setStrokeColorRGB(0.90,0.90,0.90)
      c.rect(8.25*cm,(11.77-esp2)*cm,2*cm,1*cm, fill=1) # original
      #der/izq - up/down - agranda/achica horizontal - agranda/achica vertical
      c.setFillColorRGB(0,0,0)
      c.setFont("Helvetica", 10)

      revisar = -1
      if list_names[e] in variables:
        revisar = variables[list_names[e]]
      c.drawCentredString((13.8+esp)*cm, (12.4-esp2)*cm, str('{:,}'.format(int(revisar))))
      esp = esp + 2.5

    dic = {}    
    if points[w][0]:
      dic = eval(points[w][1])
    if 'location_name' not in dic:
      dic['location_name']='-'

    if(len(dic['location_name']) > 21): # si es mas largo que 21 caracteres
      for letra in dic['location_name']: # ciclo que recorre location_name
        if(len(nombre_final) < 21):  # mientras sea menor a 21
          nombre_final = nombre_final + letra  # sigue agregando letras hasta 21
    else:
      nombre_final = dic['location_name']  # si es menor a 21 caracteres, asigna location a variable

    c.drawString(3.5*cm, (12.4-esp2)*cm,nombre_final)
    nombre_final = '' # limpia variable

    # saca el hitscore de una funcion el modelo Point
    point = Point.objects.get(id=points[w][0])
    hit = point.get_hitscore_or_salesindex()

    if hit: # si viene hitscore
      c.drawString(8.89*cm, (12.4-esp2)*cm, str(hit))
    else:
      c.drawString(8.89*cm, (12.4-esp2)*cm, '   -')

    status = point.get_readable_status()

    if status: # si viene status
      c.drawString(10.7*cm, (12.4-esp2)*cm, status)
    else:
      c.drawString(10.7*cm, (12.4-esp2)*cm, '-')

    esp2 = esp2 + 0.5

    if(w==17 or w==40 or w==80 or w==100 or w==120 or w==140 or w==160 or w==180):

      esp2 = esp2 - 13 # para que los datos de las siguientes paginas aparezcan arriba
      c.showPage()
  # fin del primer for
  c.setFillColorRGB(0,0,0)
  c.setFont("Helvetica-Bold", 10)
  c.drawString(3.5*cm , (12.3-esp2)*cm, "__________________________________________________________________________________________________________________")
  c.setFont("Helvetica", 10)
  c.drawString(3.5*cm, (11.8-esp2)*cm, "*Scoring according to date and location")

  c.setFont("Helvetica-Bold", 10)
  c.drawString(3.5*cm, 1.9*cm, "__________________________________________________________________________________________________________________")
  c.setFont("Helvetica", 10)
  c.drawString(8*cm, 1.4*cm, "www.hit-map.com | info@hit-map.com  | +562 586 50 60 | Huérfanos 862, of. 612, Santiago")

  c.showPage()

  ruta_logo = "map/static/map/Logotipo_Hitmap.png"
  c.drawImage(ruta_logo, 640, 540, width=100, height=40, mask='auto')

  num = Reports.objects.get(url_report=file_url)
  c.setFont("Helvetica", 12)
  c.drawString(3.5*cm, 19.5*cm, "Certified: N° " + str(num.id))

  c.drawString(3.5*cm, 15*cm, "Definitions")
  seg_pag = c.beginText()
  seg_pag.setTextOrigin(3.5*cm, 14*cm)
  seg_pag.setFont("Helvetica", 10)
  seg_pag.textLines(''' Hitscore is a statistical projection index, based on current average sales of open stores (100). This means that if a Histcore is 120 that
  location, according to a statistical profile, could sell 20% over average. The hitscore is meant to easily inform decision-makers by synthetizing
  hundreds of variables in one indicator that allows to rank new locations with current ones. For more information, info@hit-map.com.
  ''')
  c.drawText(seg_pag)

  c.setFont("Helvetica", 12)
  c.drawString(3.5*cm, 11.5*cm, "Metodology")

  seg_pag2 = c.beginText()
  seg_pag2.setTextOrigin(3.5*cm,10.5*cm)
  seg_pag2.setFont("Helvetica", 10)
  seg_pag2.textLines('''Hitmap algorythm values more tha 180 urban variables from multiple certified sources, and use them all to understand how the urban enviroment
  is explaining current sales (more details at www.hit-map.com). With this information, Hitmap can do a statistical projection of sale on new locations
  where data is available.

  The variables selected are the 5 more representative of different urban dimensions that can describe the location valued, and the consuming patterns.
  However, the projection -Hitscore- is done considering all variables, their wheights and combinations.
  ''')
  c.drawText(seg_pag2)

  c.setFont("Helvetica", 12)
  c.drawString(3.5*cm, 6.6*cm, "Certification")

  seg_pag3 = c.beginText()
  seg_pag3.setTextOrigin(3.5*cm,5.5*cm)
  seg_pag3.setFont("Helvetica", 10)
  seg_pag3.textLines('''The certification number at the top left of the Location Report, is a control system though wich you validate this is a true document. To do
  this ,you have to enter www.hit-map.com or right to info@hit-map.com.
  ''')
  c.drawText(seg_pag3)

  c.setFont("Helvetica-Bold", 10)
  c.drawString(3.5*cm, 1.9*cm, "_________________________________________________________________________________________________________________")
  c.setFont("Helvetica", 10)
  c.drawString(8*cm, 1.4*cm, "www.hit-map.com | info@hit-map.com  | +562 586 50 60 | Huérfanos 862, of. 612, Santiago")

  c.save()
  return url


