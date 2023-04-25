from django.apps import AppConfig

class ApiConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'api'

	def ready(self):
		import api.signals
		from api.weather_api import update_weather_data
		from apscheduler.schedulers.background import BackgroundScheduler
		scheduler = BackgroundScheduler()
		scheduler.add_job(update_weather_data, 'interval', hours=1)
		if not scheduler.running:
			# print("Station sheduler started. Interval = 1 hour")
			scheduler.start()