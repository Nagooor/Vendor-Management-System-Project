# Generated by Django 4.2.6 on 2024-05-02 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='average_response_time',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='quality_rating_avg',
        ),
        migrations.AddField(
            model_name='vendor',
            name='quality_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='vendor',
            name='response_time',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='fulfillment_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='on_time_delivery_rate',
            field=models.FloatField(default=0),
        ),
    ]
