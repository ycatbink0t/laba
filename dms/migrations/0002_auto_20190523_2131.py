# Generated by Django 2.2 on 2019-05-23 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routes',
            name='time_arrive',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='routes',
            name='time_departure',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='routes',
            name='type',
            field=models.CharField(max_length=20),
        ),
    ]
