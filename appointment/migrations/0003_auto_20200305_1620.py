# Generated by Django 3.0.2 on 2020-03-05 16:20

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_auto_20200304_0336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='uid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, unique=True),
        ),
    ]
