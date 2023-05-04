
from .models import Sensor, Station, Source, MeteoData, Profile
import django_filters
from django_filters.widgets import CSVWidget

class SensorTypeFilter(django_filters.CharFilter):
    def filter(self, qs, value):
        if value:
            sensor_types = value.split(",")
            for sensor_type in sensor_types:
                qs = qs.filter(content__icontains=sensor_type)
            return qs
        return qs


class MeteoDataFilter(django_filters.FilterSet):
    date_time_from = django_filters.DateTimeFilter(field_name='date_time', lookup_expr='gte')
    date_time_to = django_filters.DateTimeFilter(field_name='date_time', lookup_expr='lte')
    source = django_filters.AllValuesMultipleFilter(field_name='source__title', widget=CSVWidget())
    source_id = django_filters.AllValuesMultipleFilter(field_name='source__id', widget=CSVWidget())
    station = django_filters.AllValuesMultipleFilter(field_name='station__location', widget=CSVWidget())
    station_id = django_filters.AllValuesMultipleFilter(field_name='station__id', widget=CSVWidget())
    sensor = SensorTypeFilter(field_name='content')
    year = django_filters.NumberFilter(field_name='date_time__year')
    month = django_filters.NumberFilter(field_name='date_time__month')
    day = django_filters.NumberFilter(field_name='date_time__day')

    class Meta:
        model = MeteoData
        fields = ['year', 'month', 'day', 'date_time_from', 'date_time_to', 'source', 'source_id',
                  'sensor', 'station', 'station_id']


class SourceFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    sensor = django_filters.ModelMultipleChoiceFilter(
        queryset=Sensor.objects.all(),
        field_name='station__sensors__name',
        to_field_name='name',
        widget=CSVWidget(),
    )
    sensor_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Sensor.objects.all(),
        field_name='station__sensors__id',
        to_field_name='id',
        widget=CSVWidget(),
    )

    class Meta:
        model = Source
        fields = ['title', 'sensor', 'sensor_id']