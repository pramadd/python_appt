from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^appointments$', views.appointments),
    url(r'^add$', views.add),  
    url(r'^edit/(?P<number>\d+)$', views.edit),
    url(r'^update/(?P<number>\d+)/(?P<id>\d+)$', views.update),
    url(r'^delete/(?P<number>\d+)$', views.delete),
    url(r'^logout$', views.logout)
]