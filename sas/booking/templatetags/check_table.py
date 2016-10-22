from django import template

register = template.Library()


@register.assignment_tag
def check_table(cell_table, id):
    aux = 0

    for idx_hour, book in cell_table:
        if idx_hour == id:
            aux = 1
            booking = book
    if aux == 1:
        return booking
    else:
        return 'Livre.'
