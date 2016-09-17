from .models import Booking
from table import Table
from table.columns import Column

class MyBookingTable(Table):
    booking = Column(field='name')
    actions = Column(field='action')

    class Meta:
        model = Booking
