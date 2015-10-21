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
  help = 'Make a hitscore model for a project_id and save it'

  def add_arguments(self, parser):
    parser.add_argument('project_id', nargs=1, type=int)

  def handle(self, *args, **options):
    try:
      project_id = options['project_id'][0]
      project = Project.objects.get(pk=project_id)
      SimpleLog(category='starting management command', message='starting make_hitscore_model, project_id=%d' %project_id).save()
      if project.computing_model:
        SimpleLog(category='ending management command', message='model already been computed, project_id=%d' %project_id).save()
        sys.exit()
      #HERE ONLY I CAN COMPUTE A HITSCORE MODEL (NO ONE ELSE CAN)
      project.computing_model = True
      project.model_msg = "A model is been computed. We will mail you when it is finished."
      project.updated = False
      project.save()

      #CHECK CONDITIONS
      points = Point.objects.filter(project=project).exclude(sales__isnull=True)
      if len(points) < 3:
        project.computing_model = False
        project.model_msg = "No model (need more points)"
        project.save()
        SimpleLog(category='ending management command', message='no enough points with sales, project_id=%d' %project_id).save()
        sys.exit()
      geocodepoint = [p.geocode for p in points]
      geodata = Geodata.objects.filter(geocode__in=geocodepoint).exclude(var='{}')
      geocodegeodata = [g.geocode for g in geodata]
      total = filter(lambda x: True if x in geocodegeodata else False, geocodepoint)
      total = len(list(total))
      if total < 3:
        project.computing_model = False
        project.model_msg = "No model (need more points)"
        project.save()
        SimpleLog(category='ending management command', message='no enough points with geocode, project_id=%d' %project_id).save()
        sys.exit()

      #STARTING POINT WHERE I COMPUTE A HITSCORE MODEL 

      #valid models to invalid
      hm = HitscoreModel.objects.filter(valid=True).filter(project=project)
      for h in hm:
        h.valid=False
        h.save()
      new_hm = HitscoreModel(project = project)
      new_hm.save()

      dirname, filename = os.path.split(os.path.abspath(__file__))
      rscriptfile = dirname + '/HitscoreModel.R'

      param = ['Rscript', rscriptfile, str(project_id), str(new_hm.id)]
      p = Popen(param, stdin=PIPE, stdout=PIPE, stderr=PIPE)
      out, err = p.communicate()
      rc = p.returncode
      if rc == 0:
        
        project = Project.objects.get(pk=project_id)
        project.computing_model = False
        project.model_msg = 'Your model is up to date'
        project.save()
        new_hm = HitscoreModel.objects.get(pk=new_hm.id)
        new_hm.valid=True
        new_hm.save()
        SimpleLog(category='ending management command', message='ending make_hitscore_model, project_id=%d' %project_id).save()
      else:
        project = Project.objects.get(pk=project_id)
        project.computing_model = False
        project.model_msg = 'Something was wrong with your model'
        project.save()
        SimpleLog(category='ending management command', message='ending make_hitscore_model with error, project_id=%d' %project_id).save()
        ExceptionError(app="project", view="make_hitscore_model.py", message=err, var="{project_id:%d}" %project_id).save()


    except Exception as e:
      ExceptionError(app="project", view="make_hitscore_model.py", message=str(e), var="{project_id:%d}" %project_id).save()
      project = Project.objects.get(pk=project_id)
      project.computing_model = False
      project.model_msg = 'Something was wrong with your model'
      project.save()

