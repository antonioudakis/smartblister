# Generated by Django 3.0.7 on 2020-10-22 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacist', '0003_auto_20201022_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charge',
            name='charge_date',
            field=models.DateField(blank=True),
        ),
    ]
