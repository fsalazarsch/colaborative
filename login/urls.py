from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/$', views.user, name='user'),
    url(r'^useradd/$', views.useradd, name='useradd'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signout/$', views.signout, name='signout'),
    url(r'^reset$', views.reset, name='reset'),
    url(r'^terms$',views.terms, name='terms'),
]

