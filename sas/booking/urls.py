from django.conf.urls import url
from django.contrib import admin
from .views import new_user,index,list_user

urlpatterns = [	
  url(r'^/newuser/', new_user, name = 'newuser'),
  url(r'^/listuser/', list_user, name = 'listuser'), 
]
