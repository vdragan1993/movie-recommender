from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logged/$', views.logged, name='logged'),
    url(r'^logout/(?P<user_id>[0-9]+)/$', views.logout, name='logout'),
]