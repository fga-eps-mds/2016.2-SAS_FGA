from django.conf.urls import url
from django.contrib import admin
from .views import new_user, login_user, logout_user
from .views import delete_user, list_user, edit_user
from .views import new_booking

urlpatterns = [
    url(r'newuser/', new_user, name='newuser'),
    url(r'login/', login_user, name='login'),
    url(r'logout/', logout_user, name='logout'),
    url(r'delete/$', delete_user, name='deleteuser'),
	url(r'^edituser/$', edit_user, name='edituser'),
    url(r'^newbooking/$', new_booking, name='newbooking')
]
