from django.conf.urls import url
from django.contrib import admin
from .views import new_booking
from .views import search_booking
from .views import SearchBookingQueryView
from .views import search_booking_table
from .views import confirm_booking
from .views import cancel_booking
from .views import delete_booking
from .views import delete_booktime
from .views import all_bookings
from .views import pending_bookings
from .views import approve_booking
from .views import deny_booking
from .views import show_booktimes

urlpatterns = [
    url(r'^newbooking/$',
        new_booking, name='newbooking'),
    url(r'^searchbooking/$',
        search_booking, name='searchbooking'),
    url(r'^confirmbooking/(\d+)$',
        confirm_booking, name='confirmbooking'),
    url(r'^cancelbooking/(\d+)$',
        cancel_booking, name='cancelbooking'),
    url(r'^searchbookingquery/$',
        SearchBookingQueryView.as_view(),
        name='searchbookingquery'),
    url(r'^searchbookingg/$',
        SearchBookingQueryView.as_view(), name='searchbookingtable'),
    url(r'^deletebooking/(\d+)$',
        delete_booking, name='deletebooking'),
    url(r'^approvebooking/(\d+)$',
        approve_booking, name='approvebooking'),
    url(r'^denybooking/(\d+)$',
        deny_booking, name='denybooking'),
    url(r'^deletebooktime/(\d+)/(\d+)$',
        delete_booktime, name='deletebooktime'),
    url(r'^allbookings/$',
        all_bookings, name='allbookings'),
    url(r'^pendingbookings/$',
        pending_bookings, name='pendingbookings'),
    url(r'^showbooktimes/(\d+)$',
        show_booktimes, name='showbooktimes'),
]
