# Generated by Django 4.2.3 on 2023-10-14 21:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_prometheus.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("base", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FilmwebTop250",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("year", models.IntegerField()),
                ("rank", models.PositiveIntegerField(unique=True)),
                ("poster_path", models.URLField(blank=True, max_length=500, null=True)),
                (
                    "original_title",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                django_prometheus.models.ExportModelOperationsMixin("filmweb"),
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="IMDBTop250",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("year", models.IntegerField()),
                ("rank", models.PositiveIntegerField(unique=True)),
                ("poster_path", models.URLField(blank=True, max_length=500, null=True)),
            ],
            options={
                "abstract": False,
            },
            bases=(
                django_prometheus.models.ExportModelOperationsMixin("imdb"),
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="OscarWinner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("release_year", models.IntegerField(blank=True, null=True)),
                ("title", models.CharField(max_length=255)),
                ("studio", models.CharField(max_length=255)),
                ("year", models.CharField(max_length=20)),
                ("poster_path", models.URLField(blank=True, max_length=500, null=True)),
            ],
            options={
                "abstract": False,
            },
            bases=(
                django_prometheus.models.ExportModelOperationsMixin("oscar_winner"),
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="PersonList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("description", models.CharField(default="", max_length=500)),
                ("persons", models.ManyToManyField(to="base.person")),
                (
                    "user",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                django_prometheus.models.ExportModelOperationsMixin("person_list"),
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="OscarNomination",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("release_year", models.IntegerField(blank=True, null=True)),
                ("title", models.CharField(max_length=255)),
                ("studio", models.CharField(max_length=255)),
                (
                    "winner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="nominations",
                        to="list_management.oscarwinner",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                django_prometheus.models.ExportModelOperationsMixin("oscar_nomination"),
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="MovieList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("description", models.CharField(default="", max_length=500)),
                ("movies", models.ManyToManyField(to="base.movie")),
                (
                    "user",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                django_prometheus.models.ExportModelOperationsMixin("movie_list"),
                models.Model,
            ),
        ),
    ]
