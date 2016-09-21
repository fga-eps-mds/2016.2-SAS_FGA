from django.conf.urls import url
from django.contrib import admin
from .views import new_user, login_user, logout_user
from .views import delete_user, list_user, edit_user
from .views import change_password
from .views import new_booking, search_booking
from .views import confirm_booking, cancel_booking

urlpatterns = [
    url(r'newuser/', new_user, name='newuser'),
    url(r'login/', login_user, name='login'),
    url(r'logout/', logout_user, name='logout'),
    url(r'delete/$', delete_user, name='deleteuser'),
    url(r'^edituser/$', edit_user, name='edituser'),
    url(r'^change/$', change_password, name='changepassword'),
    url(r'^newbooking/$', new_booking, name='newbooking'),
    url(r'^searchbooking/$', search_booking, name='searchbooking'),
    url(r'^confirmbooking/(\d+)$', confirm_booking, name='confirmbooking'),
    url(r'^cancelbooking/(\d+)$', cancel_booking, name='cancelbooking'),
]
