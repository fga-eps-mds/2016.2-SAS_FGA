from django.conf.urls import url
from .views import logout_user
from .views import delete_user
from .views import search_user
from .views import make_user_an_admin
from .views import LoginView, ChangePasswordView
from .views import settings
from .views import NewUserView, EditUserView

urlpatterns = [
    url(r'newuser/', NewUserView.as_view(), name='newuser'),
    url(r'login/', LoginView.as_view(), name='login'),
    url(r'logout/', logout_user, name='logout'),
    url(r'delete/$', delete_user, name='deleteuser'),
    url(r'^edituser/$', EditUserView.as_view(), name='edituser'),
    url(r'^change/$', ChangePasswordView.as_view(), name='changepassword'),
    url(r'^searchuser/$', search_user, name='searchuser'),
    url(r'^settings/$', settings, name='settings'),
    url(r'^usertoadmin/(\d+)$', make_user_an_admin, name='usertoadmin'),
]
