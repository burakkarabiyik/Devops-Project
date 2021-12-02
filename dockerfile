FROM python:3.8.12
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
COPY ./Blog-Django /code/
WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
# RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'password', 'ad','soyad',25)" | python manage.py shell