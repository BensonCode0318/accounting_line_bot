# Generated by Django 3.0.4 on 2020-04-19 03:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line', '0006_remove_linerecord_recorddate'),
    ]

    operations = [
        migrations.AddField(
            model_name='linerecord',
            name='recordDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
