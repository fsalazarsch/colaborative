from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create_project$', views.create_project, name='create_project'),
    url(r'^add_point$', views.add_point, name='add_point'),
    url(r'^delete_point$', views.delete_point, name='delete_point'),
    url(r'^get_points$', views.get_points, name='get_points'),
    url(r'^get_point_sales$', views.get_point_sales, name='get_point_sales'),
   
    url(r'^get_hitscore$', views.get_hitscore, name='get_hitscore'),
    url(r'^predict_hitscore$', views.predict_hitscore, name='predict_hitscore'),
    url(r'^get_points_information$', views.get_points_information, name='get_points_information'),
    url(r'^get_point_data$', views.get_point_data, name='get_point_data'),
    url(r'^make_hitscore_model$', views.make_hitscore_model, name='make_hitscore_model'),
    url(r'^project_model_message$', views.project_model_message, name='project_model_message'),
    url(r'^update_point_sales$', views.update_point_sales, name='update_point_sales'),
    url(r'^update_point_notes$', views.update_point_notes, name='update_point_notes'),
    url(r'^(?P<project_id>-?\d+)/$', views.edit_project, name='index'),
    url(r'^projectuser_set_permissions/$', views.projectuser_set_permissions, name='projectuser_set_permissions'),
    url(r'^add_user/$', views.add_user, name='add_user'),
    url(r'^delete_user/$', views.delete_user, name='delete_user'),
    url(r'^change_point_status/$', views.change_point_status, name='change_point_status'),
    url(r'^set_location_name/$', views.set_location_name, name='set_location_name'),
    url(r'^get_point_report/$', views.get_point_report, name='get_point_report'),
    url(r'^get_project_report/$', views.get_project_report, name='get_project_report'),
    url(r'^delete_project/$', views.delete_project, name='delete_project'),
]
