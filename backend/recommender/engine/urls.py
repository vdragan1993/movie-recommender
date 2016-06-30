from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logged/$', views.logged, name='logged'),
    url(r'^logout/(?P<user_id>[0-9]+)/$', views.logout, name='logout'),
    url(r'^profile/(?P<user_id>[0-9]+)/$', views.profile, name='profile'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^insert/$', views.insert, name='insert'),
    url(r'^delete/(?P<service_id>[0-9]+)/$', views.delete, name='delete'),
]