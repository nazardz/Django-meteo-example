from rest_framework import serializers
from .models import Sensor, Station, Source, MeteoData, Profile, SourceAccess
import requests


class SourceAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceAccess
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor
        fields = '__all__'


class StationSerializer(serializers.ModelSerializer):
    # sensors = SensorSerializer(many=True, read_only=True)
    # sensors = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='sensors.all')
    sensors_count = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = '__all__'

    def validate_geo_pointer(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("geo_pointer should be a dictionary.")
        if 'latitude' not in value or 'longitude' not in value:
            raise serializers.ValidationError("geo_pointer should have 'latitude' and 'longitude' keys.")
        if not isinstance(value['latitude'], (float, int)) or not isinstance(value['longitude'], (float, int)):
            raise serializers.ValidationError("latitude and longitude should be numbers.")
        return value

    def get_sensors_count(self, obj):
        return obj.sensors.count()


class StationNestSerializer(serializers.ModelSerializer):
    sensors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Station
        fields = ['id', 'location', 'sensors']


class SourceSerializer(serializers.ModelSerializer):
    location = serializers.CharField(source='station.location', read_only=True)
    sensors = serializers.StringRelatedField(source='station.sensors', many=True, read_only=True)

    class Meta:
        model = Source
        fields = ['id', 'title', 'station', 'location', 'sensors', 'access']
    # class Meta:
    #     model = Source
    #     fields = '__all__'


class MeteoDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeteoData
        fields = '__all__'

    def create(self, validated_data):

        user = self.context['request'].user
        try:
            source_data = validated_data['source']

            if not user.profile.sources.filter(pk=source_data.pk).exists():
                raise serializers.ValidationError('User does not have access to this source.')

            station = source_data.station
            ip_address = station.ip_address
            ip_port = station.ip_port
            if not ip_port or ip_port == 0:
                url = f"http://{ip_address}"
            else:
                url = f"http://{ip_address}:{ip_port}"
            try:
                response = requests.get(url)
                content = response.json()

                filtered_content = {}
                for sensor_type, sensor_value in content.items():
                    if sensor_type in station.sensors.values_list('name', flat=True):
                        filtered_content[sensor_type] = sensor_value

                meteo_data = MeteoData.objects.create(content=filtered_content, source=source_data, station=station)

                station.meteodata_list.add(meteo_data)
                station.save()


                #if user.is_authenticated:
                profile = user.profile
                profile.request_count += 1
                profile.save()

                return meteo_data
            except Exception as e:
                print(e)
                raise serializers.ValidationError("Could not connect to source {}".format(source_data))
        except AttributeError as e:
            print(e)
            raise serializers.ValidationError("Provide valid Source")

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

