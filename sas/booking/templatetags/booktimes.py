from django import template
from booking.models import Booking

register = template.Library()


@register.filter(name='order_booktimes')
def order_booktimes(booking):
    return booking.time.order_by('date_booking')
