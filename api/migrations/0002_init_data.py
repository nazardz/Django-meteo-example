from django.db import migrations


def add_data(apps, schema_editor):
    Model = apps.get_model('api', 'Sensor')
    Model.objects.create(name='sensPressure')
    Model.objects.create(name='sensPm25')
    Model.objects.create(name='sensDhtTemp')
    Model.objects.create(name='sensDhtHumidity')
    Model.objects.create(name='sens18b20Temp')

    Access = apps.get_model('api', 'SourceAccess')
    Access.objects.create(name='Public', level=1)
    Access.objects.create(name='Private', level=2)
    Access.objects.create(name='Test', level=3)

    Station = apps.get_model('api', 'Station')
    Station.objects.create(location='Test Megacam', ip_address="192.168.204.68", ip_port=8015,
                           geo_pointer={'latitude': 0.0, 'longitude': 0.0})
    station = Station.objects.get(id=1)
    station.sensors.set([1, 2, 3, 4, 5])


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_data),
    ]
