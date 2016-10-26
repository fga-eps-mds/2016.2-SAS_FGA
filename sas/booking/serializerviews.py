from booking.models import Place, Building
from rest_framework import viewsets
from rest_framework import generics
from booking.serializers import PlaceSerializer
from booking.serializers import BuildingSerializer

class PlaceViewSet(viewsets.ModelViewSet):
    
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

class BuildingViewSet(viewsets.ModelViewSet):
    
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

class BuildingPlaceList(generics.ListAPIView):
    serializer_class = PlaceSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        id_building = self.kwargs['id_building']
        building = Building.objects.get(pk=id_building)
        return Place.objects.filter(building=building)


