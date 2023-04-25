from django.contrib import admin
from .models import Sensor, Station, Source, MeteoData, Profile, SourceAccess


class SourceAccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level')


class SensorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'ip_address', 'ip_port', 'geo_pointer')


class SourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'station', 'access')


# class MeteoDataAdmin(admin.ModelAdmin):
#     list_display = ('id', 'date_time', 'source')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'request_count', 'access_level')


admin.site.register(Sensor, SensorAdmin)
admin.site.register(Station, StationAdmin)
admin.site.register(Source, SourceAdmin)
#admin.site.register(MeteoData, MeteoDataAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(SourceAccess, SourceAccessAdmin)