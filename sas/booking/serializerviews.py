from booking.models import Place
from rest_framework import viewsets
from booking.serializers import PlaceSerializer

class PlaceViewSet(viewsets.ModelViewSet):
    
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer



