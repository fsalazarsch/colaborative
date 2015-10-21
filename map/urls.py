from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^temp$', views.temp, name='temp'),
    url(r'^score_board$', views.score_board, name='score_board'),
    url(r'^get_point_scoreboard$', views.get_point_scoreboard, name='get_point_scoreboard'),
]


