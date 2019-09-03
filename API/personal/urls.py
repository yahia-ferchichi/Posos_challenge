from django.conf.urls import include, url

from . import views #importing from the current package

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^result/$', views.calculateProba, name='calculate'),
]   

