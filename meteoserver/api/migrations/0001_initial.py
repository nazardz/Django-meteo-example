# Generated by Django 4.2 on 2023-04-24 11:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MeteoData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('content', models.JSONField(default=dict, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Test Sensor', max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SourceAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Public', max_length=100, unique=True)),
                ('level', models.IntegerField(default='0', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(default='Test Location', max_length=100)),
                ('ip_address', models.GenericIPAddressField(default='192.168.204.68', protocol='IPv4')),
                ('ip_port', models.IntegerField(null=True)),
                ('geo_pointer', models.JSONField(default={'latitude': 0.0, 'longitude': 0.0})),
                ('meteodata_list', models.ManyToManyField(default=None, editable=False, related_name='stations', to='api.meteodata')),
                ('sensors', models.ManyToManyField(to='api.sensor')),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('access', models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='access', to='api.sourceaccess')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sources', to='api.station')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_level', models.IntegerField(auto_created=1, default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('request_count', models.IntegerField(auto_created=0, default=0, editable=False)),
                ('sources', models.ManyToManyField(to='api.source')),
                ('user', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='meteodata',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data', to='api.source'),
        ),
        migrations.AddField(
            model_name='meteodata',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='api.station'),
        ),
    ]
