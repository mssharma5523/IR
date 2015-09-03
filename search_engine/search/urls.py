from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^test/(?P<page>.*)', views.staticpage),
	url(r'^search/index\.html$', views.index),
	# url(r'^search/(?P<query>\.*)$', views.index, name='index'),
]