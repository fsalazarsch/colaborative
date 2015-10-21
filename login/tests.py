from django.test import TestCase
from .utils import validate_email

class ValidateEmailTestCase(TestCase):
  def validate(self):
    self.assertEqual(validate_email(''), False)
    self.assertEqual(validate_email('larry'), False)
    self.assertEqual(validate_email('@'), False)
    self.assertEqual(validate_email('hit-map'), False)
    self.assertEqual(validate_email('.'), False)
    self.assertEqual(validate_email('com'), False)
    self.assertEqual(validate_email('larry@'), False)
    self.assertEqual(validate_email('larryhit-map'), False)
    self.assertEqual(validate_email('larry.'), False)
    self.assertEqual(validate_email('larrycom'), False)
    self.assertEqual(validate_email('@hit-map'), False)
    self.assertEqual(validate_email('@.'), False)
    self.assertEqual(validate_email('@com'), False)
    self.assertEqual(validate_email('hit-map.'), False)
    self.assertEqual(validate_email('hit-mapcom'), False)
    self.assertEqual(validate_email('.com'), False)
    self.assertEqual(validate_email('larry@hit-map'), False)
    self.assertEqual(validate_email('larry@.'), False)
    self.assertEqual(validate_email('larry@com'), False)
    self.assertEqual(validate_email('larryhit-map.'), False)
    self.assertEqual(validate_email('larryhit-mapcom'), False)
    self.assertEqual(validate_email('larry.com'), False)
    self.assertEqual(validate_email('@hit-map.'), False)
    self.assertEqual(validate_email('@hit-mapcom'), False)
    self.assertEqual(validate_email('@.com'), False)
    self.assertEqual(validate_email('hitmap.com'), False)
    self.assertEqual(validate_email('larry@hit-map.'), False)
    self.assertEqual(validate_email('larry@hit-mapcom'), False)
    self.assertEqual(validate_email('larry@.com'), False)
    self.assertEqual(validate_email('larryhit-map.com'), False)
    self.assertEqual(validate_email('@hit-map.com'), False)
    self.assertEqual(validate_email('larry@hit-map.com'), True)



