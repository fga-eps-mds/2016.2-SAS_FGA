from booking.models import Place, Building
from rest_framework import serializers


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Place
        fields = ("name", "pk")

class BuildingSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Building
        fields = ("name", "pk")

