# Generated by Django 4.2.3 on 2023-08-09 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_remove_movielist_list_type_remove_movielist_people_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personlist',
            name='persons',
        ),
        migrations.RemoveField(
            model_name='personlist',
            name='user',
        ),
        migrations.DeleteModel(
            name='MovieList',
        ),
        migrations.DeleteModel(
            name='PersonList',
        ),
    ]
