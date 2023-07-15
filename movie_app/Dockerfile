FROM python:3.12.0b4-bookworm

#setting working directory
WORKDIR /app

#env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECIDE 1

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]