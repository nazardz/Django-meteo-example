FROM python:3.9-slim-buster
WORKDIR /code
COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py makemigrations
RUN python manage.py migrate
COPY ./api/migrations/0002_init_data.py ./api/migrations/
RUN python manage.py migrate
RUN echo "from django.contrib.auth.models import User; User.objects.filter(username='root').exists() or User.objects.create_superuser('root', 'root@example.com', 'admin')" | python manage.py shell
EXPOSE 8080
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8081"]
