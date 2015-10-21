from map.models import *
from map.ray_casting import point_in_poly
from math import sqrt, pow


point = [-70.650777, -33.439521]


def distance(p1, p2):
  return sqrt(pow((p1[0]-p2[0]),2) + pow((p1[1]-p2[1]),2))


for geo in geocodes:
  vertices = eval(geo.vertices)
  if point_in_poly(point, vertices):
    print("success!")
    print(geo.id)


for geo in geocodes:
  cent = eval(geo.centroid)
  if distance(cent, point) < 0.1:
    print(geo.id)


