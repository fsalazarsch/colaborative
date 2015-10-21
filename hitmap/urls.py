from django.conf.urls import include, url
from django.contrib import admin
from login.views import index

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^map/', include('map.urls', namespace='map')),
    url(r'^login/', include('login.urls', namespace='login')),
    url(r'^project/', include('project.urls', namespace='project')),
    url(r'^chaintype/', include('chaintype.urls', namespace='chaintype')),
    url(r'^$', index, name='index'),
]
