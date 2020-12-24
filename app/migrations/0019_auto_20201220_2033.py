# Generated by Django 2.2.12 on 2020-12-21 01:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20201220_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2020, 12, 20, 20, 33, 57, 135002), verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2020, 12, 20, 20, 33, 57, 135999), verbose_name='Дата'),
        ),
    ]