# Generated by Django 3.1.3 on 2021-06-09 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0018_auto_20210331_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inflow',
            name='source_account_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='inflow',
            name='source_account_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='inflow',
            name='source_account_provider',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='inflow',
            name='usd_paid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='inflow',
            name='usd_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='outflow',
            name='dest_account_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='outflow',
            name='dest_account_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='outflow',
            name='dest_account_provider_code',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='outflow',
            name='dest_account_provider_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
