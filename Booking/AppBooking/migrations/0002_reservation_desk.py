# Generated by Django 5.1.7 on 2025-03-28 10:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppBooking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='desk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppBooking.desk'),
        ),
    ]
