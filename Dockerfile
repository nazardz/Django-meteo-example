FROM python:3.8-slim-buster
COPY . .
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8081
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN echo "from django.contrib.auth.models import User; User.objects.filter(username='root').exists() or User.objects.create_superuser('root', 'admin@example.com', 'admin')" | python manage.py shell
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8081"]
