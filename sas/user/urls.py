from django.conf.urls import url
from .views import new_user, login_user, logout_user
from .views import delete_user, edit_user
from .views import change_password, search_user
from .views import make_user_an_admin

urlpatterns = [
    url(r'newuser/', new_user, name='newuser'),
    url(r'login/', login_user, name='login'),
    url(r'logout/', logout_user, name='logout'),
    url(r'delete/$', delete_user, name='deleteuser'),
    url(r'^edituser/$', edit_user, name='edituser'),
    url(r'^change/$', change_password, name='changepassword'),
    url(r'^searchuser/$', search_user, name='searchuser'),
    url(r'^usertoadmin/(\d+)$', make_user_an_admin, name='usertoadmin'),
]
