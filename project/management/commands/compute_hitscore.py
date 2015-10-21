from django.core.management.base import BaseCommand, CommandError
from map.models import Geocode, Geodata
from login.models import ExceptionError, SimpleLog
from project.models import Project, Point, HitscoreModel
import sys
import os
from subprocess import Popen, PIPE
#
#from https://docs.djangoproject.com/en/1.8/howto/custom-management-commands/
#

#
# NOTA: si dos objetos se recuperan y ambos actualizan campos distintos
# los cambios se sobreescriben
#

#SE ASUME QUE SOLO SE CREA EL MODELO UNA VES

class Command(BaseCommand):
  help = 'Compute a hitscore value'

  def add_arguments(self, parser):
    parser.add_argument('hitscoremodel_id', nargs=1, type=int)
    parser.add_argument('point_id', nargs=1, type=int)

  def handle(self, *args, **options):
    try:
      hitscoremodel_id = options['hitscoremodel_id'][0]
      point_id = options['point_id'][0]
      print(hitscoremodel_id, point_id)

      SimpleLog(category='starting management command', message='starting compute_hitscore.R, hitscoremodel_id=%d, point_id=%d' %(hitscoremodel_id, point_id)).save()

      dirname, filename = os.path.split(os.path.abspath(__file__))
      rscriptfile = dirname + '/compute_hitscore.R'

      #off the grid
      if hitscoremodel_id < 0:
        print('of the grid')
        rscriptfile = dirname + '/compute_hitscore_off_the_grid.R'
        param = ['Rscript', rscriptfile, str(hitscoremodel_id), str(point_id)]
        p = Popen(param, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        print(out)
        print(err)
        print("ending computing hitscore")
        sys.exit()

      param = ['Rscript', rscriptfile, str(hitscoremodel_id), str(point_id)]
      p = Popen(param, stdin=PIPE, stdout=PIPE, stderr=PIPE)
      out, err = p.communicate()
      rc = p.returncode
      print(out)
      print(err)

    except Exception as e:
      SimpleLog(category='ending management command', message='ending compute_hitscore.R with error, hitscoremodel_id=%d, point_id=%d' %(hitscoremodel_id, point_id)).save()
      ExceptionError(app="project", view="compute_htiscore.py", message=err, var="{hitscoremodel_id:%d, point_id:%d}" %(hitscoremodel_id, point_id)).save()
      
      

