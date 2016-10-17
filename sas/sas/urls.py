from django.conf.urls import url, include
from django.contrib import admin
from .views import index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name = "index"),
    url(r'^user/', include('user.urls', namespace="user")),
    url(r'^booking/', include('booking.urls', namespace="booking")),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
