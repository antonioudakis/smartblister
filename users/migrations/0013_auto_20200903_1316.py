# Generated by Django 3.0.7 on 2020-09-03 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_patientprofile_doctor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientprofile',
            name='AMKA',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='amka',
            field=models.CharField(default='', max_length=11, unique=True),
        ),
    ]
