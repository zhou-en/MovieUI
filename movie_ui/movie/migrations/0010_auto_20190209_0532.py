# Generated by Django 2.1.5 on 2019-02-09 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0009_auto_20190209_0529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]