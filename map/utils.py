import time
from PIL import Image
from urllib.request import urlopen

#[float, float], [[float, float]] -> bool
#[lat,long] [[lat,long]] -> bool
#True if point within polygon
def point_in_poly(latlon,poly):
  x = latlon[0]
  y = latlon[1]
  # check if point is a vertex
  if (x,y) in poly: return True
  # check if point is on a boundary
  for i in range(len(poly)):
    p1 = None
    p2 = None
    if i==0:
      p1 = poly[0]
      p2 = poly[1]
    else:
      p1 = poly[i-1]
      p2 = poly[i]
    if p1[1] == p2[1] and p1[1] == y and x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
      return True
  n = len(poly)
  inside = False
  p1x,p1y = poly[0]
  for i in range(n+1):
    p2x,p2y = poly[i % n]
    if y > min(p1y,p2y):
      if y <= max(p1y,p2y):
        if x <= max(p1x,p2x):
          if p1y != p2y:
            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
          if p1x == p2x or x <= xints:
            inside = not inside
    p1x,p1y = p2x,p2y
  return True if inside else False


#area_id is a kind of index used to filter geocodes
def get_area_id(lat, lon):
  precision = 2 # if you modify this, you have to modify get_precision
  lat, lon = str(float(lat)), str(float(lon))
  lat, lon = lat.split('.'), lon.split('.')
  int_lat, dec_lat = lat[0], lat[1]
  int_lon, dec_lon = lon[0], lon[1]
  dec_lat += '0'*precision
  dec_lon += '0'*precision
  area_id = int_lat +'_'+ dec_lat[0:precision] +'_'+ int_lon +'_'+ dec_lon[0:precision]
  return area_id

def get_precision():
  return 2 # if you modify this, you have to modify get_are_id


def centroid(vertices):
  l = len(vertices)
  lat=0
  lon=0
  for a,b in vertices:
    lat += a
    lon += b
  return [lat/l,lon/l]


#lat, lont, status -> url_foto
def get_google_map_image(lat, lon, status):
  print("starting get_google_map_image")
  # llama a un mapa de static map de google y lo guarda
  url = "https://maps.googleapis.com/maps/api/staticmap?"
  url += "key=AIzaSyD1lNt_uSfHEq1Q8UR9fUJPq123BouDSDQ"
  url += "&center=%f,%f" %(lat, lon)
  url += "&zoom=18&size=1024x1024"
  url += "&maptype=roadmap"
  url += "&style=feature:transit%7Celement:labels.icon%7Cvisibility:off"
  url += "&style=feature:poi%7Cvisibility:off"
  url += "&style=feature:landscape%7Celement:labels.icon%7Cvisibility:off"
  url += "&style=feature:landscape%7Celement:labels.text%7Ccolor:0xffffff"
  url += "&style=feature:road%7Celement:labels.icon%7Cvisibility:off"
  url += "&style=feature:road.highway%7Celement:geometry%7Ccolor:0xD2D3D0"
  url += "&markers=icon:http://165.225.151.107/static/project/images/"+status+"|%f,%f" %(lat, lon)
                        
  ret = "/tmp/hitmap-" + str(time.time()) + ".png"
  fd = urlopen(url)
  im = Image.open(fd)
  im.save(ret)
  print("ending get_google_map_image")
  return ret

