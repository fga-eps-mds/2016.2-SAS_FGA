from django.conf.urls import url
from .views import new_user, logout_user
from .views import delete_user, edit_user
from .views import search_user
from .views import make_user_an_admin
from .views import LoginView, ChangePasswordView

urlpatterns = [
    url(r'newuser/', new_user, name='newuser'),
    url(r'login/', LoginView.as_view(), name='login'),
    url(r'logout/', logout_user, name='logout'),
    url(r'delete/$', delete_user, name='deleteuser'),
    url(r'^edituser/$', edit_user, name='edituser'),
    url(r'^change/$', ChangePasswordView.as_view(), name='changepassword'),
    url(r'^searchuser/$', search_user, name='searchuser'),
    url(r'^usertoadmin/(\d+)$', make_user_an_admin, name='usertoadmin'),
]
