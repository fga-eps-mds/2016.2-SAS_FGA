from django.conf.urls import url
from django.contrib import admin
from .views import new_user,list_user,edit_user

urlpatterns = [	
	url(r'^newuser/$', new_user, name = 'newuser'),
  	url(r'^listuser/$', list_user, name = 'listuser'),
  	url(r'^edituser/(?P<id>\d+)/$', edit_user, name = 'edituser'), 
]
