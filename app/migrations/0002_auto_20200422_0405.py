# Generated by Django 2.2.12 on 2020-04-22 01:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2020, 4, 22, 4, 5, 32, 606007), verbose_name='Опубликовано'),
        ),
    ]
