# Generated by Django 3.0.7 on 2021-01-31 11:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacist', '0016_auto_20210130_0850'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlisterAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_removed', models.DateTimeField(default=django.utils.timezone.now)),
                ('blisterPrescription', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pharmacist.BlisterPrescription')),
            ],
        ),
    ]
