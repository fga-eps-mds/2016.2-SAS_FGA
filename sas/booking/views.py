from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm, SearchBookingForm
from .models import Booking, BookTime, Place, Building
from django.contrib import messages
from sas.views import index
from datetime import datetime, timedelta

def search_booking_query(request):
    form_booking = SearchBookingForm()
    if request.method == "POST":
        form_booking = SearchBookingForm(request.POST)
        option = request.POST.get('search_options')
        if not(form_booking.is_valid()):
            return render(request, 'booking/searchBookingQuery.html',
                                    {'search_booking': form_booking})
        elif(option == 'opt_day_room'):S
            #view method from who was responsable for this table - Fabiola
        elif(option == 'opt_booking_week'):
            pass
            #view method from who was responsable for this table - Meu
        elif(option == 'opt_building_day'):
            pass
            #view method from who was responsable for this table - Hugo
        else:
            return (search_booking_room_period(request,form_booking))
            #view method from who was responsable for opt_room_period table - Luis
    return render(request, 'booking/searchBookingQuery.html',
                            {'search_booking': form_booking})

def search_booking_room_period(request,form_booking):
    bookings = form_booking.search()
    form_days = form_booking.days_list()
    place_id = form_booking["room_name"].data
    booking_place = Place.objects.get(id = place_id)

    cont= timedelta(hours=0)
    auxs = []
    days = []
    rows = []
    time = []
    aux=0
    table =[]
    skip = 0
    aux_rows = []
    
    for form_day in form_days:
        i=0              
        for booktime in BookTime.objects.filter(date_booking = str(form_day)):
            if booktime is not None:
                booking = Booking.objects.get(time__pk = booktime.pk)
                if (booking.place.name == booking_place.name):
                    if (booktime.date_booking <= form_days[-1]) and (booktime.date_booking >= form_days[0]):
                        
                        for i in range(0,12):
                            #print('book',booktime.start_hour.timedelta())
                            print('cont',cont)                            
                            if (booktime.start_hour == cont):
                                print('ue')
                                time.insert(i,cont)
                                i += 1
                                aux = 1
                            cont += timedelta(hours=2)
                            aux = 0
                        cont = timedelta(hours=0)        

                        days.append(booktime.date_booking)
                        aux_rows.append(booking.name)
                        skip += 1 
                            
        
        if aux == 1:
            print('aux_rows',aux_rows)
            rows.insert(i,aux_rows)
        
        aux_rows = []
        aux_rows = next(skip,aux_rows)    
        
        aux = 0
    i=0
    aux_table = []

    for times in time:
        aux_table = []
        if times:
            aux_table.append(times)
            for row in rows[i]:  
                aux_table.append(row)
            i+=1        
        table.append(aux_table)        

    print('table',table)    

    return render(request, 'booking/template_table.html', {'days' : days, 'table':table})

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
