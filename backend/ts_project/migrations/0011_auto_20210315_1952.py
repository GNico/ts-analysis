# Generated by Django 3.1.5 on 2021-03-15 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ts_project', '0010_periodicanalysis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='periodicanalysis',
            name='id',
        ),
        migrations.AlterField(
            model_name='periodicanalysis',
            name='analysis',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='ts_project.analysis'),
        ),
        migrations.AlterField(
            model_name='periodicanalysis',
            name='time_interval',
            field=models.TextField(),
        ),
    ]
