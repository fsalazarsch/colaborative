### README

#### System Requirements
* Python3.4
* Django 1.8.1
* PostgreSQL 9.4

#### Other libraries
* docopt==0.6.2
* docutils==0.12
* Flask==0.10.1
* grip==3.3.0
* gunicorn==19.3.0
* vitsdangerous==0.24
* Jinja2==2.7.3
* Markdown==2.6.2
* MarkupSafe==0.23
* path-and-address==1.0.0
* Pillow==2.8.1
* psycopg2==2.6
* Pygments==2.0.2
* reportlab==3.1.44
* requests==2.7.0
* uWSGI==2.0.10
* validate-email==1.3
* virtualenv==13.1.0
* Werkzeug==0.10.4


#### API
> **pony.myhitmap.com/login/user/** a testear  
> **pony.myhitmap.com/login/user/add/** a testear  
> **pony.myhitmap.com/login/signin/** a testear  
> **pony.myhitmap.com/login/signout/** a testear  
> **pony.myhitmap.com/project/project/** a desarrollar  
> **pony.myhitmap.com/project/user/** a desarrollar  
> **pony.myhitmap.com/project/point/** a desarrollar  
> **pony.myhitmap.com/project/model/** a desarrollar  
> **pony.myhitmap.com/project/point/urbandata/** a desarrollar  
> **pony.myhitmap.com/project/point/yelp/** a desarrollar  
> **pony.myhitmap.com/project/point/hitscore/** a desarrollar  
> **pony.myhitmap.com/chaintype/typelist** a desarrollar  
> **pony.myhitmap.com/chaintype/subtypelist** a desarrollar  

##### login
> **pony.myhitmap.com/login/user/**
> > <pre><code>method = GET  
> > GET()</code></pre>  
> > Retorna una descripcion detallada del usuario logueado  
> > <pre><code>{"status":"OK",  
> >  "msg":"",  
> >  "user":{"id":1, 
> >          "first_name":"Larry",  
> >          "last_name:":"Gonzalez",  
> >          "email:":"larry@hit-map.com"}  
> > </code></pre>  
* * *
> > <pre><code>method = PUT  
> > POST(...)</code></pre>  
> > Actualiza los valores dados en post del usuario logueado. Puede tomar valores de: first_name, last_name, password(para la actualizacion del mismo), new_password(debe ir acompañado de password)  
> > <pre><code>{"status":"OK",  
> >  "msg":""}  
> > </code></pre>  
* * *
> > <pre><code>method = DELETE  
> > POST(user_id(int))</code></pre>  
> > Deja al usuario no activo.  
> > <pre><code>{"status":"OK",  
> >  "msg":""}  
> > </code></pre>  

> **pony.myhitmap.com/login/user/add/**
> > <pre><code>method = POST  
> > POST(first_name(str), last_name(str), email(str), password(str), terms(str))</code></pre>  
> > csrf_exempt. Crea un usuario con los valores dados. Por el momento crea un proyecto inicial y lo asocia al usuario. Valida que todos los parametros tengan alguna letra, el email no este registrado, term sea 'true'  
> > <pre><code>{"status":"OK",  
> >  "msg":""}  
> > </code></pre>  



> **pony.myhitmap.com/login/signin/**
> > <pre><code>method = POST
> > POST(email(str), password(str))</code></pre>  
> > csrf_exempt. Crea la session si el usuario es valido y activo. Qué cosas guardaremos?
> > <pre><code>{"status":"OK",  
> >  "msg":"user logged in"}
> > </code></pre>  

> **pony.myhitmap.com/login/signout/**  
> > <pre><code>method not used</code></pre>  
> > Desloguea al usuario  
> > <pre><code>{"status":"OK",  
> >  "msg":"user logged out"}
> > </code></pre>  

##### project
> **pony.myhitmap.com/project/project/**
> > <pre><code>method = GET  
> > GET</code></pre>  
> > Recupera al usuario por session. Retorna la lista de proyectos que el usuario tiene permisis para ver. Filtra los proyectos eliminados (is_visible=True).  
> > <pre><code>{"status":"OK",  
> >  "msg":"",  
> >  "total":2,  
> >  "projects":[{"id":1, "name":"initial project"},  
> >              {"id":2, "name":"second project"}]}  
> > </code></pre>  
* * *
> > <pre><code>method = GET  
> > GET(project_id)</code></pre>  
> > Recupera al usuario por session, toma el project_id del request, valida que el usuario tenga permiso de lectura sobre el proyecto, que sea visible y retorna la descripcion del proyecto.  
> > <pre><code>{"status":"OK",  
> >  "msg":"",  
> >  "project":{"id":1, 
> >             "name":"initial project",
> >             "owner":1,
> >             "points":5,
> >             "wizard_open":-1}}  
> > </code></pre>
* * *
> > <pre><code>method = POST  
> > POST(name(str))</code></pre>  
> > Recupera al usuario por session. Crea un nuevo proyecto asociado al usuario. Valida que el usuario no sea dueño de un proyecto con el mismo nombre. Retorna el id del nuevo proyecto.  
> > <pre><code>{"status":"OK",  
> >  "msg":"",
> >  "project_id":34}  
> > </code></pre>  
* * *
> > <pre><code>method = PUT  
> > POST(project_id(int), ...)</code></pre>  
> > Recupera al usuario por session, toma el project_id y los valores a cambiar del request, valida que el usuario tenga permiso de escritura sobre el proyecto, que sea visible y actualiza los atributos del proyecto. Puede tomar valores "name", "wizard_open"  
> > <pre><code>{"status":"OK",  
> >  "msg":""}  
> > </code></pre>  
* * *
> > <pre><code>method = DELETE  
> > POST(project_id(int))</code></pre>  
> > Recupera al usuario por session y el project_id del request, valida que el usuario sea dueño sobre el proyecto, que sea visible e invisibiliza al proyecto (is_visible=False).
> > <pre><code>{"status":"OK",  
> >  "msg":""}  
> > </code></pre>  

> **pony.myhitmap.com/project/user/**
> > <pre><code>method = GET  
> > GET(project_id(int))</code></pre>  
> > Retorna los id de los usuarios que tienen acceso al proyecto y su permiso asociado (read, write, owner)  
> > <pre><code>{"status":"OK",  
> >  "msg":"",  
> >  "users":[{"id":2, "user_id":2, "permission":"owner"}, 
> >           {"id":3, "user_id":3, "permission":"read"}]}  
> > </code></pre>  
* * *
> > <pre><code>method = POST  
> > POST(project_id(int), user_id(int))</code></pre>  
> > Recupera al usuario por sesion. Habilita al usuario pasado por parametro para que vea el proyecto  
> > <pre><code>{"status":"OK",  
> >  "msg":""}  
> > </code></pre>
* * *
> > <pre><code>method = PUT  
> > POST(project_id(int), user_id(int), permission)</code></pre>  
> > Cambia el permiso del usuario pasado por parametro en el proyecto. si permission es 0, se elimina al usuario del proyecto.
> > <pre><code>{"status":"OK",  
> >  "msg":""}  
> > </code></pre>  

> **pony.myhitmap.com/project/point/**
> > <pre><code>method = GET  
> > GET(project_id)</code></pre>  
> > Recupera al usuario por sesion y el project_id del request. Valida que el usuario tenga permiso de lectura sobre el proyecto. Retorna la lista de puntos que pertenecen al proyecto  
> > <pre><code>{"status":"OK",  
> >  "msg":"",  
> >  "total":2,  
> >  "points":[{"id":1, "location_name":"huerfanos"},  
> >              {"id":2, "location_name":"moneda"}]}  
> > </code></pre>  
* * *
> > <pre><code>method = GET  
> > GET(project_id(int), point_id(int))</code></pre>  
> > Recupera al usuario por sesion, el project_id y el point_id del request. Valida que el usuario tenga permiso de lectura sobre el proyecto. Valida que el punto pertenezca al proyecto. Retorna la descripcion detallada del punto  
> > <pre><code>{"status":"OK",  
> >  "msg":"",  
> >  "total":2,  
> >  "point":{"id":1, "location_name":"huerfanos", "latitude":-30.234, "longitude":-70.456}}  
> > </code></pre>  
* * *
> > <pre><code>method = POST  
> > POST(project_id(int), latitude, longitude)</code></pre>  
> > Recupera al usuario por sesion, el project_id, latitude y longitude del request. Valida que el usuario tenga permiso de escritura sobre el proyecto. Crea un punto asociado al proyecto. Retorna el point_id.  
> > <pre><code>{"status":"OK",  
> >  "msg":"",
> >  "point_id":25}  
> > </code></pre>  
* * *
> > <pre><code>method = PUT  
> > POST(project_id(int), point_id(int), ...)</code></pre>  
> > Recupera al usuario por sesion, el project_id, point_id, y ... del request. Valida que el usuario tenga permiso de escritura sobre el proyecto. Actualiza el punto con los valores dados. Puede tomar valores de (COMPLETAR).
> > <pre><code>{"status":"OK",  
> >  "msg":""}  
> > </code></pre>  
* * *
> > <pre><code>method = DELETE  
> > POST(project_id(int), point_id(int))</code></pre>  
> > Recupera al usuario por sesion, el project_id y el point_id del request. Valida que el usuario tenga permiso de escritura sobre el proyecto. Invisibiliza el punto.
> > Invisibiliza al punto en el proyecto.  
> > <pre><code>{"status":"OK",  
> >  "msg":""}  
> > </code></pre>  

> **pony.myhitmap.com/project/point/urbandata/**
> > <pre><code>method = GET  
> > GET(project_id(int), point_id(int))</code></pre>  
> > Recupera al usuario por sesion, el project_id y el point_id del request. Valida que el usuario tenga permiso de lectura sobre el proyecto. Retorna la data urbana asociada al proyecto.  
> > <pre><code>{"status":"OK",  
> >  "msg":"",  
> >  "data":{"point_id":25,
> >          "poi_101":2,
> >          "adt_101":3}}  
> > </code></pre>  

> **pony.myhitmap.com/project/point/yelp/**
> > <pre><code>method = GET  
> > GET(category(str))</code></pre>  
> > Recupera al usuario por sesion y la categoria del request. Valida que el usuario tenga permiso de lectura sobre el proyecto. Retorna los puntos de yelp de esa categoria.  
> > <pre><code>{"status":"OK",  
> >  "msg":"",  
> >  "data":{"point_id":25,
> >          "poi_101":2,
> >          "adt_101":3}}  
> > </code></pre>  

> **pony.myhitmap.com/project/point/hitscore/**  
> > <pre><code>method = GET  
> > GET(project_id(int), point_id(int))</code></pre>  
> > Recupera al usuario por sesion, el project_id y el point_id del request. Valida que el usuario tenga permiso de lectura sobre el proyecto. Retorna el hitscore del punto. Si tiene permisos de escritura, lo calcula de ser necesario.  
> > <pre><code>{"status":"OK",  
> >  "msg":"",  
> >  "hitscore":110}  
> > </code></pre>  

> **pony.myhitmap.com/project/model/**  
> > <pre><code>method = GET  
> > GET(project_id(int))</code></pre>  
> > Recupera al usuario por sesion, el project_id del request. Valida que el usuario tenga permiso de lectura sobre el proyecto. Retorna estadisticas asociadas al hitscoremodel  
> > <pre><code>{"status":"OK",  
> >  "msg":"",  
> >  "data":{"open_locations":2, "accuracy":97.3}}(COMPLETAR)  
> > </code></pre>  
* * *
> > <pre><code>method = POST  
> > POST(project_id(int))</code></pre>  
> > Recupera al usuario por sesion, el project_id del request. Valida que el usuario tenga permiso de escritura sobre el proyecto. Calcula un nuevo modelo hitscoremodel  
> > <pre><code>{"status":"OK",  
> >  "msg":""}  
> > </code></pre>  

##### chaintype
> **pony.myhitmap.com/chaintype/typelist**  
> > <pre><code>method = GET  
> > GET</code></pre>  
> > Recupera al usuario por sesion. Retorna la lista de categorias que puede tomar un proyecto  
> > <pre><code>{"status":"OK",  
> >  "msg":"",  
> >  "data":["Anchors", "Stores", "Pop-Up", "Other"]}  
> > </code></pre>  


> **pony.myhitmap.com/chaintype/subtypelist**  
> > <pre><code>method = GET  
> > GET(chaintype(str)=None)</code></pre>  
> > Recupera al usuario por sesion. Retorna una lista con las subcategorías asociadas a chaintype. Retorna todas las subchaintype si chaintype no esta definido  
> > <pre><code>{"status":"OK",  
> >  "msg":"",  
> >  "data":["Other"]}  
> > </code></pre>  


