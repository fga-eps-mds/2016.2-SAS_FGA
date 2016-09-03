from django.conf.urls import url
from django.contrib import admin
from .views import new_user

urlpatterns = [
    url(r'newuser/', new_user, name = 'newuser'),

]
