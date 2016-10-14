from django.conf.urls import url
from django.contrib import admin
from .views import new_booking, search_booking, search_booking_query, search_booking_table
from .views import confirm_booking, cancel_booking
from .views import confirm_booking, cancel_booking, delete_booking

urlpatterns = [
    url(r'^newbooking/$', new_booking, name='newbooking'),
    url(r'^searchbooking/$', search_booking, name='searchbooking'),
    url(r'^confirmbooking/(\d+)$', confirm_booking, name='confirmbooking'),
    url(r'^cancelbooking/(\d+)$', cancel_booking, name='cancelbooking'),
	url(r'^searchbookingquery/$', search_booking_query, name='searchbookingquery'),
	url(r'^searchbookingg/$', search_booking_query, name='searchbookingtable'),
    url(r'^deletebooking/(\d+)$', delete_booking, name='deletebooking'),
]
