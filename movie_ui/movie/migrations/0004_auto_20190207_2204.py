# Generated by Django 2.1.5 on 2019-02-07 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_auto_20190207_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='imdb_id',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
