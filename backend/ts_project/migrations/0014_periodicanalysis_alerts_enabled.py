# Generated by Django 3.1.5 on 2021-03-18 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ts_project', '0013_auto_20210316_0204'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodicanalysis',
            name='alerts_enabled',
            field=models.BooleanField(default=False),
        ),
    ]
