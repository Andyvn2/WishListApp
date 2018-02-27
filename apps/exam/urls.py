from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^main$', views.index),
	url(r'^login$', views.login),
	url(r'^register', views.register),
	url(r'^dashboard$', views.home),
	url(r'^wish_items/create$', views.createpage),
	url(r'^new_wishlist$', views.NewItem),
	url(r'^remove/(?P<id>\d+)$', views.remove),
	url(r'^item/(?P<id>\d+)$', views.item),
	url(r'^logout$', views.logout),
	url(r'^add/(?P<id>\d+)$', views.add),
	url(r'^delete/(?P<id>\d+)$', views.delete)


	]