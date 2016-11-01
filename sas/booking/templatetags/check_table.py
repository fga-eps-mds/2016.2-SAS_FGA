from django import template

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
