from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm, SearchBookingForm
from .models import Booking, BookTime, Place, Building
from django.contrib import messages
from sas.views import index
from datetime import datetime, timedelta
import operator
from collections import OrderedDict

def search_booking_query(request):
    form_booking = SearchBookingForm()
    if request.method == "POST":
        form_booking = SearchBookingForm(request.POST)
        option = request.POST.get('search_options')
        if not(form_booking.is_valid()):
            return render(request, 'booking/searchBookingQuery.html',
                                    {'search_booking': form_booking})
        elif(option == 'opt_day_room'):
            pass
            #view method from who was responsable for this table - Fabiola
        elif(option == 'opt_booking_week'):
            pass
            #view method from who was responsable for this table - Meu
        elif(option == 'opt_building_day'):
            #view method from who was responsable for this table - Hugo
            return (search_booking_building_day(request,form_booking))
        else:
            return (search_booking_room_period(request,form_booking))
            #view method from who was responsable for opt_room_period table - Luis
    return render(request, 'booking/searchBookingQuery.html',
                            {'search_booking': form_booking})

def search_booking_building_day(request,form_booking):
    hours = [(6,"06-08"),(8,"08-10"),(10,"10-12"),(12,"12-14"),(14,"14-16"),(16,"16-18"),(18,"18-20"),(20,"20-22"),(22,("22-00"))]
    form_day = form_booking.get_day()
    building_id = form_booking["building_name"].data
    building = Building.objects.get(id = building_id)
    places = Place.objects.filter(building = building)
    n = len(places) +1

    places_ = []
    table =[]

    for place in places:
        aux =[]
        bookings = Booking.objects.filter(time__date_booking=str(form_day))
        for booking in bookings:
            if (booking.place.name == place.name):
                book = booking.time.get(date_booking = str(form_day))
                aux_tuple = (book.start_hour.hour,booking.name)
                aux.append(aux_tuple)

        table.append(aux)

        p = place.name.split('-')
        places_.append(p[1])

    return render(request, 'booking/template_table.html', {'days':places_, 'table':table, 'hours':hours, 'n':n, 'name': "Building x Day"})

def search_booking_room_period(request,form_booking):
    form_days = form_booking.days_list()
    place_id = form_booking["room_name"].data
    booking_place = Place.objects.get(id = place_id)
    hours = [(6,"06-08"),(8,"08-10"),(10,"10-12"),(12,"12-14"),(14,"14-16"),(16,"16-18"),(18,"18-20"),(20,"20-22"),(22,("22-00"))]
    n = len(form_days) + 1

    table =[]

    for form_day in form_days:
        aux =[]
        bookings = Booking.objects.filter(time__date_booking=str(form_day))
        for booking in bookings:
            if (booking.place.name == booking_place.name):
                book = booking.time.get(date_booking = str(form_day))
                print('hours',book.start_hour.hour)
                print('booking name', booking.name)
                aux_tuple = (book.start_hour.hour,booking.name)
                aux.append(aux_tuple)

        table.append(aux)

    return render(request, 'booking/template_table.html', {'days':form_days, 'table':table, 'hours':hours, 'n':n, 'name': "Room x Period"})

def next(skip,aux_rows):
    for i in range(skip):
        aux_rows.append(" ")
    return aux_rows

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
        if request.user.profile_user.is_admin():
            bookings = Booking.objects.all()
        else:
            bookings = Booking.objects.filter(user=request.user)
        return render(request, 'booking/searchBooking.html', {'bookings': bookings})
    else:
        return redirect("index")

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

def delete_booking(request, id):
	if request.user.has_permission_to_delete() and request.session['booking']:
		id = int(id)
		if id == request.session.get('booking'):
			request.session.pop('booking')
			Booking.objects.get(pk=id).delete()
			messages.success(request, _('Booking deleted!'))
		else:
			messages.error(request, _('You cannot delete this booking.'))
	else:
		messages.error(request, _('You cannot delete this booking.')) 
