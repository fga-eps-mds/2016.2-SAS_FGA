from django import template
from django.utils.translation import ugettext_lazy as _
import datetime

register = template.Library()


@register.filter(name='get_timetable')
def get_timetable(booking):
    weekdays = [0, 1, 2, 3, 4, 5, 6]
    timetable = []
    # ASSUMED FIRST 7 SEVEN ITEMS CAN IDENTIFY TIMETABLE
    book_times = booking.time.all().order_by('date_booking')[:7]
    for book_time in book_times:
        try:
            weekdays.remove(book_time.date_booking.weekday())
            weekday = _(book_time.date_booking.strftime("%A"))
            weekday_time = (book_time.start_hour, book_time.end_hour)
            timetable.append((weekday, weekday_time))
        except ValueError:
            break
    return timetable


@register.filter(name='status_glyphicon')
def status_glyphicon(booking):
    STATUS = ((0, "glyphicon-remove"), (1, "glyphicon-option-horizontal"),
              (2, "glyphicon-ok"))
    try:
        return STATUS[booking.status][1]
    except:
        return None


@register.filter(name='is_all_bookings')
def is_all_bookings(name):
    if name == _('All Bookings'):
        return True
    else:
        return False

@register.filter(name='is_false')
def is_false(arg): 
    return arg is False