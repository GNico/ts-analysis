# Generated by Django 3.1.5 on 2021-05-17 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ts_project', '0020_auto_20210507_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodicanalysis',
            name='last_run',
            field=models.DateTimeField(null=True),
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anomalies', models.JSONField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('periodic_analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='ts_project.periodicanalysis')),
            ],
            options={
                'db_table': 'results',
            },
        ),
    ]
