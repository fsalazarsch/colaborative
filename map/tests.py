from django.test import TestCase

from map.models import point_in_poly


def test_point_in_poly_pacman_inside(self):
  """
  point_in_poly should return False for points
  inside the convex poligon
  """
  pacman = [[-33.445814, -70.660100], [-33.436682, -70.635327], [-33.431270, -70.660080], [-33.438110, -70.649566]]
  point_inside = [-33.437502, -70.640683]
  self.assertEqual(point_in_poly(point_inside,pacman), True)


def test_point_in_poly_pacman_outside(self):
  """
  point_in_poly should return False for points
  ouside the convex poligon
  """
  pacman = [[-33.445814, -70.660100], [-33.436682, -70.635327], [-33.431270, -70.660080], [-33.438110, -70.649566]]
  point_outside = [-33.437573, -70.657463]
  self.assertEqual(point_in_poly(point_outside,pacman), False)


