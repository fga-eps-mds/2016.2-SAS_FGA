from django.conf.urls import url
from django.contrib import admin
from booking.views import (new_booking, search_booking, SearchBookingQueryView,
                            search_booking_table, confirm_booking,
                            cancel_booking, delete_booking, delete_booktime,
                            all_bookings)

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
    url(r'^deletebooktime/(\d+)/(\d+)$',
        delete_booktime, name='deletebooktime'),
    url(r'^allbookings/$',
        all_bookings, name='allbookings'),
]
