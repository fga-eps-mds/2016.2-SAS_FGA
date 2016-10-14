from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking, BookTime, Place, Building
from .forms import BookingForm, SearchBooking, SearchBookingForm
from django.contrib import messages
from sas.views import index
from datetime import datetime, timedelta

def search_booking_query(request):
	form_booking = SearchBookingForm()
	return render(request, 'booking/searchBookingQuery.html',
							{'search_booking': form_booking})

def new_booking(request):
	if request.user.is_authenticated():
		if request.method == "POST":
			form_booking = BookingForm(request.POST)
			if (form_booking.is_valid()):
				booking = form_booking.save(request.user)
				if booking:
					request.session['booking'] = booking.pk
					return render(request, 'booking/showDates.html',
									{'booking': booking})
				else:
					messages.error(request, _("Booking alread exists"))
		else:
			form_booking = BookingForm()

		return render(request, 'booking/newBooking.html',
							{'form_booking': form_booking})
	else:
		return index(request)

def search_booking_table(request):
	if request.method == "POST":
		form_booking = SearchBooking(request.POST)
		if(form_booking.is_valid()):
			bookings = form_booking.search()
			return render(request, 'booking/template_table.html', {'form_booking' : form_booking, 'bookings' : bookings})
		else:
			return render(request, 'booking/searchBookingTable.html', {'form_booking' : form_booking})
	else:
		form_booking = SearchBooking()
		return render(request, 'booking/searchBookingTable.html', {'form_booking' : form_booking})

def search_booking(request):
    if request.user.is_authenticated():
        bookings = Booking.objects.filter(user=request.user)
        return render(request, 'booking/searchBooking.html',
						{'bookings': bookings})
    else:
        form = LoginForm()
        return render(request, 'booking/index.html', {'form': form})


def cancel_booking(request, id):
	if request.user.is_authenticated() and request.session['booking']:
		id = int(id)
		if(id == request.session.get('booking')):
			request.session.pop('booking')
			Booking.objects.get(pk=id).delete()
			messages.success(request, _("Booking has been canceled"))
			return index(request)
		else:
			messages.error(request, _("You cannot cancel this booking"))
			return index(request)
	else:
		return index(request)


def confirm_booking(request, id):
	if request.user.is_authenticated() and request.session.get('booking'):
		id = int(id)
		if id == request.session.get('booking'):
			request.session.pop('booking')
			messages.success(request, _("Booking has been saved."))
			return index(request)
		else:
			messages.error(request, _("You cannot confirm this booking"))
			return index(request)
	else:
		return index(request)
