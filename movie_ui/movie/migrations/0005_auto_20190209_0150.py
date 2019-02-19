# Generated by Django 2.1.5 on 2019-02-09 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_auto_20190207_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='filename',
            field=models.CharField(default=None, max_length=256, unique=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb_movie_url',
            field=models.CharField(default=None, max_length=256),
        ),
    ]