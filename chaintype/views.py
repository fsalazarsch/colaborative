from django.core import serializers
from django.http import JsonResponse
from chaintype.models import ChainType, ChainSubType


def typelist(request):
  """retorna la lista de categorias de proyectos"""
  if request.method == 'GET':
    ct = ChainType.objects.all()
    ct = [str(c) for c in ct]
    return JsonResponse({'status':'OK', 'data':ct})
  else:
    return JsonResponse({'status':'ERROR', 'msg':'invalid http method'})

  
def subtypelist(request):
  """retorna la lista subcategorias de proyectos"""
  if request.method == 'GET':
    try:
      chaintype = request.GET['chaintype']
    except:
      chaintype = ''

    if chaintype:
      try:
        ct = ChainType.objects.get(name=chaintype)
        cst = ChainSubType.objects.filter(chaintype=ct)
      except:
        return JsonResponse({'status':'ERROR', 'msg':'invalid chaintype'})
    else:
      cst = ChainSubType.objects.all()
    cst = [str(c) for c in cst]
    return JsonResponse({'status':'OK', 'data':cst})
  else:
    return JsonResponse({'status':'ERROR', 'msg':'invalid http method'})


