FROM python:3.8-slim-buster
COPY . .
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8080"]
