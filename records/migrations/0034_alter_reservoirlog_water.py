# Generated by Django 4.0.4 on 2023-05-07 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0033_remove_reservoirlog_ro_reservoirlog_reverse_osmosis_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservoirlog',
            name='water',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
