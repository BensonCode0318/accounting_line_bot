# Generated by Django 3.0.4 on 2020-04-19 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LineRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.TextField(blank=True, null=True)),
                ('recordType', models.IntegerField(blank=True, null=True)),
                ('recordContent', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
