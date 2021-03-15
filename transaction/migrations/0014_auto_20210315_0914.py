# Generated by Django 3.1.3 on 2021-03-15 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0013_inflow_usd_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='inflow',
            name='fee',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='outflow',
            name='fee',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
    ]
