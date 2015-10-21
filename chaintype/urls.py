from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^typelist$', views.typelist, name='typelist'),
    url(r'^subtypelist$', views.subtypelist, name='subtypelist'),
]

