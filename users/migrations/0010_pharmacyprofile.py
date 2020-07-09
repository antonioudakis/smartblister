# Generated by Django 3.0.7 on 2020-07-09 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0009_pharmacistprofile_doy'),
    ]

    operations = [
        migrations.CreateModel(
            name='PharmacyProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('tax_num', models.CharField(max_length=9)),
                ('doy', models.CharField(default='', max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('address_no', models.SmallIntegerField()),
                ('TK', models.SmallIntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
