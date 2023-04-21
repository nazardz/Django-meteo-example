from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class SourceAccess(models.Model):
	name = models.CharField(max_length=100, default="Public", unique=True)
	level = models.IntegerField(default="0", unique=True)

	def __str__(self):
		return self.name

class Sensor(models.Model):
	name = models.CharField(max_length=100, default="Test Sensor", unique=True)

	def __str__(self):
		return self.name

class Station(models.Model):
	location = models.CharField(max_length=100, default="Test Location")
	ip_address = models.GenericIPAddressField(protocol='IPv4', default="192.168.204.68")
	sensors = models.ManyToManyField(Sensor)
	ip_port = models.IntegerField(null=True)
	geo_pointer = models.JSONField(default=dict({'latitude': 0.0, 'longitude': 0.0}))
	meteodata_list = models.ManyToManyField('MeteoData', default=None, editable=False, related_name='stations')

	def __str__(self):
		return self.location

class Source(models.Model):
	title = models.CharField(max_length=100)
	station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='sources')
	access = models.ForeignKey(SourceAccess, on_delete=models.DO_NOTHING, related_name='access', default=0)

	def __str__(self):
		return self.title

class MeteoData(models.Model):
	date_time = models.DateTimeField(auto_now_add=True, editable=False)
	content = models.JSONField(default=dict, editable=False)
	source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='data')


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
	request_count = models.IntegerField(default=0, auto_created=0, editable=False)
	sources = models.ManyToManyField(Source)
	access_level = models.IntegerField(default=0, auto_created=0)


