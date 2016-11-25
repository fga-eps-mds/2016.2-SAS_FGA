from booking.models import Place, Building
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from booking.serializers import PlaceSerializer
from booking.serializers import BuildingSerializer
from rest_framework.decorators import detail_route

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

class UnoccupiedPlaceList(viewsets.ViewSet):

    @detail_route(methods=["post"])
    def list(self, request):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """

        if 'id_building' in request.POST:        
            id_building = request.POST['id_building']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            start_hour = request.POST['start_hour']
            end_hour = request.POST['end_hour']
            weekday = request.POST['weekday[]']

            places = Place.objects.filter(
                building_id = id_building, 
                booking_place__time__date_booking__gte = start_date, 
                booking_place__time__date_booking__lt = end_date, 
                booking_place__time__start_hour = start_hour, 
                booking_place__time__end_hour = end_hour, 
                booking_place__time__date_booking__week_day__in = weekday
            ).distinct()

            unoccupied = Place.objects.filter(building_id=id_building).exclude(pk__in=places)

        else:
            unoccupied = Place.objects.all()

        serializer = PlaceSerializer(unoccupied, many=True)
        return Response(serializer.data)
