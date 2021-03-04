# Generated by Django 3.1.3 on 2021-03-04 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0012_inflow_usd_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='inflow',
            name='usd_paid',
            field=models.DecimalField(decimal_places=2, max_digits=14, null=True),
        ),
    ]
