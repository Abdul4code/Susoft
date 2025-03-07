# Generated by Django 4.2.13 on 2025-03-06 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('token', models.CharField(editable=False, max_length=255, unique=True)),
                ('description', models.TextField()),
            ],
        ),
    ]
