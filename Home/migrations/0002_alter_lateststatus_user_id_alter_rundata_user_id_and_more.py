# Generated by Django 4.2 on 2023-05-16 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lateststatus',
            name='user_id',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='rundata',
            name='user_id',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='sitdata',
            name='user_id',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='sportsinfo',
            name='user_id',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='walkdata',
            name='user_id',
            field=models.CharField(max_length=20),
        ),
    ]
