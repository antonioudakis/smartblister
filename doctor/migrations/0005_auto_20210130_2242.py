# Generated by Django 3.0.7 on 2021-01-30 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0004_auto_20210130_2032'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frequency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='prescription',
            name='frequency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='doctor.Frequency'),
        ),
    ]
