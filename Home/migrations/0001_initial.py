# Generated by Django 4.2 on 2023-05-16 05:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LatestStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('status', models.CharField(default='暂无', max_length=10)),
                ('data', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='RunData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('now_time', models.DateTimeField(validators=[django.core.validators.RegexValidator(message='Invalid datetime format. Please use the format "YYYY-MM-DD".', regex='^\\d{4}-\\d{2}-\\d{2}$')])),
                ('run_rate', models.FloatField()),
                ('run_time', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SitData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('now_time', models.DateTimeField(validators=[django.core.validators.RegexValidator(message='Invalid datetime format. Please use the format "YYYY-MM-DD".', regex='^\\d{4}-\\d{2}-\\d{2}$')])),
                ('sit_time', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SportsInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('now_time', models.DateTimeField(validators=[django.core.validators.RegexValidator(message='Invalid datetime format. Please use the format "YYYY-MM-DD".', regex='^\\d{4}-\\d{2}-\\d{2}$')])),
                ('sports_time', models.IntegerField()),
                ('steps', models.IntegerField()),
                ('heat', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WalkData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('now_time', models.DateTimeField(validators=[django.core.validators.RegexValidator(message='Invalid datetime format. Please use the format "YYYY-MM-DD".', regex='^\\d{4}-\\d{2}-\\d{2}$')])),
                ('walk_rate', models.FloatField()),
                ('walk_time', models.IntegerField()),
            ],
        ),
    ]