# Generated by Django 5.1.7 on 2025-04-01 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppBooking', '0003_reservation_desk_worker_position_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='worker',
            name='position',
        ),
    ]
