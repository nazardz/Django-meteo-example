from apscheduler.schedulers.background import BackgroundScheduler
import requests
from .models import Station, MeteoData

def update_weather_data():
	print('fetch meteodata from Stations')
	stations = Station.objects.all()
	for station in stations:
		if not station.ip_port or station.ip_port == 0:
			url = f"http://{station.ip_address}"
		else:
			url = f"http://{station.ip_address}:{station.ip_port}"
		response = requests.get(url)
		if response.status_code == 200:
			content = response.json()

			filtered_content = {}
			for sensor_type, sensor_value in content.items():
				if sensor_type in station.sensors.values_list('name', flat=True):
					filtered_content[sensor_type] = sensor_value

			# source = Source.objects.get(name='Weather API')
			meteo_data = MeteoData.objects.create(content=filtered_content, station=station)

			# station.meteodata_list.add(meteo_data)
			station.save()
