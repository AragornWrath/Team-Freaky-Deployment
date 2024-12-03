# Generated by Django 5.1.2 on 2024-10-23 14:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TripItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_name', models.CharField(max_length=100)),
                ('date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='token',
            field=models.CharField(max_length=100),
        ),
    ]