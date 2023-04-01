# Generated by Django 4.1.7 on 2023-03-30 18:05

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('store_name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=30, null=True)),
                ('active', models.BooleanField(null=True)),
                ('address', models.CharField(max_length=1000, null=True)),
                ('address_city', models.CharField(max_length=100, null=True)),
                ('address_state', models.CharField(max_length=100, null=True)),
                ('pincode', models.CharField(max_length=10, null=True)),
                ('latitude', models.DecimalField(decimal_places=5, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=5, max_digits=10)),
                ('geolocation', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
    ]