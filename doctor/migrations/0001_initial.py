# Generated by Django 3.0.7 on 2020-09-04 08:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0013_auto_20200903_1316'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitoringRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_requested', models.DateField(default=django.utils.timezone.now)),
                ('token', models.CharField(max_length=100)),
                ('accepted', models.BooleanField(default=False)),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.DoctorProfile')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.PatientProfile')),
            ],
        ),
    ]
