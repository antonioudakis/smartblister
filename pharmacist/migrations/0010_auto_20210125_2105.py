# Generated by Django 3.0.7 on 2021-01-25 19:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pharmacist', '0009_auto_20210125_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blister',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='blisterprescription',
            name='blister',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pharmacist.Blister'),
        ),
        migrations.AlterField(
            model_name='blisterprescription',
            name='prescription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pharmacist.Prescription'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
