from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^travels$' , views.travels),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^createPlan$', views.createPlan),
    url(r'^show/(?P<id>\d+)$', views.show),
    url(r'^createTrips$', views.createTrips),
    url(r'^trips$', views.trips),
    url(r'^logout$', views.logout),
    url(r'^join/(?P<trip_id>\d+)$', views.join),
    url(r'^delete/(?P<trip_id>\d+)$', views.delete),
    url(r'^cancel/(?P<trip_id>\d+)$', views.cancel),
    url(r'^back$', views.back),
    # url(r'^success$', views.success),
]