# Generated by Django 3.1.3 on 2022-01-18 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0020_auto_20210720_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inflow',
            name='source_account_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
