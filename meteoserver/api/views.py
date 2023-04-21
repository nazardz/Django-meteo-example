from rest_framework import generics
from rest_framework.authtoken.admin import User

from .models import Sensor, Station, Source, MeteoData, Profile
from .serializers import SensorSerializer, StationSerializer, SourceSerializer, MeteoDataSerializer, \
    ProfileSerializer, SourceAccessSerializer, SourceAccess
from .filters import MeteoDataFilter, SourceFilter
from django_filters.rest_framework import DjangoFilterBackend


class SensorList(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class StationList(generics.ListCreateAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

    def perform_create(self, serializer):
        sensors = self.request.data.get('sensors', [])
        station = serializer.save()
        for sensor_id in sensors:
            sensor = Sensor.objects.get(pk=sensor_id)
            station.sensors.add(sensor)


class StationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class SourceList(generics.ListCreateAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SourceFilter

    def perform_create(self, serializer):
        source = serializer.save()
        superusers = User.objects.filter(is_superuser=True)
        for user in superusers:
            profile = Profile.objects.get(user=user)
            profile.sources.add(source)




class SourceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class MeteoDataList(generics.ListCreateAPIView):
    queryset = MeteoData.objects.all()
    serializer_class = MeteoDataSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MeteoDataFilter


class MeteoDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MeteoData.objects.all()
    serializer_class = MeteoDataSerializer


class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class AccessView(generics.ListCreateAPIView):
    queryset = SourceAccess.objects.all()
    serializer_class = SourceAccessSerializer


class AccessDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SourceAccess.objects.all()
    serializer_class = SourceAccessSerializer
