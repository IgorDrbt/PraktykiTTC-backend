import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Desk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id_login', models.AutoField(primary_key=True, serialize=False)),
                ('login', models.CharField(max_length=20)),
                ('passwd', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id_worker', models.AutoField(primary_key=True, serialize=False)),
                ('name_worker', models.CharField(max_length=30)),
                ('surname_worker', models.CharField(max_length=30)),
                ('id_login', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppBooking.login')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id_number_table', models.AutoField(primary_key=True, serialize=False)),
                ('reservation_time', models.DateField()),
                ('id_worker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppBooking.worker')),
            ],
        ),
    ]
