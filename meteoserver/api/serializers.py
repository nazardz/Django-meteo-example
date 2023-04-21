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
        fields = ['location', 'sensors']


class SourceSerializer(serializers.ModelSerializer):
    access = serializers.StringRelatedField()
    station = StationNestSerializer()

    class Meta:
        model = Source
        fields = '__all__'

    def create(self, validated_data):
        # Check if the source is public
        access = validated_data.get('access')
        if access.name == 'Public':
            source = Source.objects.create(**validated_data)
            # Add the public source to existing profiles
            profiles = Profile.objects.all()
            for profile in profiles:
                profile.sources.add(source)
            return source
        else:
            return super().create(validated_data)

    def update(self, instance, validated_data):
        access = validated_data.get('access', instance.access)
        sources_with_old_access = Source.objects.filter(access=instance.access)
        sources_with_new_access = Source.objects.filter(access=access)
        profiles = Profile.objects.filter(
            sources__in=sources_with_old_access,
            access_level__lte=access.level,
        )
        for profile in profiles:
            # remove the source from the profile if it no longer matches the access level
            if instance in profile.sources.all() and instance not in sources_with_new_access:
                profile.sources.remove(instance)
            # add the source to the profile if it now matches the access level
            elif instance not in profile.sources.all() and instance in sources_with_new_access:
                profile.sources.add(instance)
        return super().update(instance, validated_data)



class MeteoDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeteoData
        fields = '__all__'

    def create(self, validated_data):

        user = self.context['request'].user
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

            meteo_data = MeteoData.objects.create(content=filtered_content, source=source_data)

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

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

