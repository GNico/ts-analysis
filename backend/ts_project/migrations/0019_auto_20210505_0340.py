# Generated by Django 3.1.5 on 2021-05-05 03:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ts_project', '0018_periodicanalysis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitor',
            name='notification_email',
        ),
        migrations.AddField(
            model_name='periodicanalysis',
            name='relevant_period',
            field=models.TextField(default='1d'),
        ),
        migrations.AlterField(
            model_name='periodicanalysis',
            name='monitor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detectors', to='ts_project.monitor'),
        ),
        migrations.CreateModel(
            name='NotificationChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('monitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_channels', to='ts_project.monitor')),
            ],
            options={
                'db_table': 'notification_channels',
            },
        ),
    ]
