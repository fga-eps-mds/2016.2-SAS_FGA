from django import template
from datetime import timedelta

register = template.Library()

@register.filter(name='check_tooltip')
def check_tooltip(cell_table, id):
    aux = 0

    for idx_hour, book in cell_table:
        if idx_hour == id:
            aux = 1
            booking = book
    if aux == 1:
        return booking.user.get_full_name()
    else:
        return None

@register.filter(name='check_table')
def check_table(cell_table, id):
    aux = 0
    for idx_hour, book in cell_table:
        if idx_hour == id:
            aux = 1
            booking = book

    if aux == 1:
   	    return booking.name
    else:
        return None

@register.filter(name='aux_search_date')
def aux_search_date(days,n):
    return days,n

@register.filter(name='search_date')
def search_date(daysn,count):
    days, n = daysn

    if count < n:        
        return days[count]

@register.filter(name='search_hour')
def search_hour(id,option):
    
    if option == 0:
        time = timedelta(hours=id)
    else:
        if id == 22:
            time = timedelta(hours=id+2) - timedelta(days=1)
        else:
            time = timedelta(hours=id+2)        

    return time