# Movie-App
## Requirements
* docker and docker compose

## Installation
Firstly, clone the repository from the github to your local folder with the following command:
```
git clone https://github.com/Milosz-cat/Movie-App.git
```

Next, create an `.env` file where the `docker-compose.yml` is and copy the content from the `.env.sample` file. Example:
```env
SECRET_KEY=ENTER_YOUR_SECRET_KEY_HERE
DEBUG=True
ALLOWED_HOSTS=127.0.0.1 0.0.0.0 localhost

TMDB_API_KEY=ENTER_YOUR_TMDB_API_KEY_HERE
BEARER=ENTER_YOUR_BEARER_HERE

EMAIL_HOST_USER = ENTER_YOUR_EMAIL_HOST_USER_HERE
EMAIL_HOST_PASSWORD = ENTER_YOUR_EMAIL_HOST_PASSWORD_HERE

DB_NAME=postgres
DB_USER=milosz
DB_PASSWORD=milosz
DB_HOST=db
```

In the same directory, where the `docker-compose.yml` is, run the following commands:
```
docker compose build
```
## Usage

Before starting docker you can create admin account:
```
docker-compose run --rm -e DJANGO_SUPERUSER_USERNAME=admin -e DJANGO_SUPERUSER_PASSWORD=admin -e DJANGO_SUPERUSER_EMAIL=admin@example.com app python manage.py createsuperuser --no-input
```

To start the container and test the api run the following command:
```
docker compose up
```

Now you can head over to http://127.0.0.1:8000/api/docs/ to test the api

To stop the container run:
```
docker compose down
```


