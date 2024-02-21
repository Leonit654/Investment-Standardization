FROM python:3

WORKDIR /usr/src/app


COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python load_initial_data.py && python manage.py runserver 0.0.0.0:8000"]
