#!/bin/python
import psycopg2
import psycopg2.extras

#host where to read data
read_host="localhost"
read_user="hitmap"
read_database="hitmap"
read_pass="hitmap"

#host where to write data
write_user="hitmap"
write_pass="hitmap"
write_database="hitmap"
write_host="localhost"

#open connection and cursors
read_con = psycopg2.connect(host=read_host, database=read_database, user=read_user, password=read_pass)
write_con = psycopg2.connect(host=write_host, database=write_database, user=write_user, password=write_pass) 
inserter = write_con.cursor()

#define a function to insert row
def insert_geodata(fetched_row):
  geocode = fetched_row['geocode']
  #delete undesired vars
  del fetched_row['objectid'] 
  del fetched_row['geocode']
  #delete keys with null values
  clean_row = {key:val for key,val in fetched_row.items() if val is not None}
  sql_insert = 'insert into map_geodata (geocode, var) values (%s, %s)'
  inserter.execute(sql_insert, ( geocode, str(clean_row).replace("'", '"' ) ) )

#execute a 'select *' on origin tables and insert results
origin_tables = [ 'hm_datos_urbanos_chile', 'hm_datos_urbanos_california', ]
for table in origin_tables:
  print('Fetching from %s ' % table)
  acum = 0
  sql_select = "select * from  %s;" % table
  fetcher = read_con.cursor('read_cursor_%s' % table, cursor_factory=psycopg2.extras.RealDictCursor) #server-side dictionary cursor.
  fetcher.execute( sql_select )
  fetched_row = fetcher.fetchone()
  while fetched_row:
    insert_geodata(fetched_row)
    acum += 1
    if (acum % 1024 == 0):
      write_con.commit()
      print('*', end="",flush=True)
    fetched_row = fetcher.fetchone()
  fetcher.close()
  print(' Done. %d rows inserted.' % acum)

#close connections
inserter.close()
read_con.close()
write_con.close()
print('Connections closed. Bye.')
