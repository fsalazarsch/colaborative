import os
import sys
import psycopg2

sys.path.append("..")
os.environ["DJANGO_SETTINGS_MODULE"] = "hitmap.settings"

from map.models import get_area_id, centroid

host = 'localhost'
port = 5432
database = 'hitmap'
user = 'hitmap'
password = 'hitmap'

con = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
cur = con.cursor()
sql = "INSERT INTO map_geocode (vertices, geocode, centroid_latitude, centroid_longitude, area_id) values ('%s', %s, '%s', '%s', '%s');"

files = ['../data/Geocode_chile.json.txt', '../data/Geocode_california.json.txt']

for f in files:
  fr = open(f, 'r')
  i=0
  for line in fr:
    i+=1
    line = line.strip()
    line = eval(line)
    geocode = line[0]
    vertices = line[1]
    latitude, longitude = centroid(vertices)
    areas = [get_area_id(v[0], v[1]) for v in vertices]
    areas = list(set(areas))
    for a in areas:
      query = sql %(str(vertices), str(geocode), str(latitude), str(longitude), str(a))
      cur.execute(query)
    if i%100==0:
      print(i)
      con.commit()
  con.commit()

