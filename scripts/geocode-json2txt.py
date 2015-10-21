import json

files = ['../data/Geocode_chile.json', '../data/Geocode_california.json']

for f in files:
  print("reading file %s" %f)
  fr = open(f, 'r')
  data = fr.read()
  print("transform to json")
  data = json.loads(data)

  print("tranforming data")
  geocode = [int(d['attributes']['geocode']) for d in data['features']]
  vertices = [d['geometry']['rings'][0] for d in data['features']]
  vertices = [list(map(lambda x: [x[1], x[0]], v)) for v in vertices]
  print("data transformed")

  fw = open(f+'.txt','w')
  l = len(geocode)
  for i in range(l):
    aux = [geocode[i], vertices[i]]
    fw.write(str(aux)+'\n')
    if i%500==0:
      print("%d de %d" %(i,l))
  fw.close()

