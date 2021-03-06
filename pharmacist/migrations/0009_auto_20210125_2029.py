# Generated by Django 3.0.7 on 2021-01-25 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pharmacist', '0008_auto_20210122_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlisterPrescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='blister',
            name='charge_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='blister',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='prescription',
            name='date_issued',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='prescription',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='ChargeBlister',
        ),
        migrations.AddField(
            model_name='blisterprescription',
            name='blister',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacist.Blister'),
        ),
        migrations.AddField(
            model_name='blisterprescription',
            name='prescription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacist.Prescription'),
        ),
    ]
