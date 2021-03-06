# Generated by Django 3.0.7 on 2020-10-25 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacist', '0006_auto_20201022_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='charge',
            name='frequency',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, '1 ανά ημέρα'), (2, '2 ανά ημέρα'), (3, '3 ανά ημέρα')], default=1),
        ),
        migrations.AddField(
            model_name='charge',
            name='medicine',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='charge',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
