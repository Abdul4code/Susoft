# Generated by Django 4.2.13 on 2025-03-06 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('susaf_susoft', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='token',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
