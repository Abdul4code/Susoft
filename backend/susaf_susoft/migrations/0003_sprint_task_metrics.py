# Generated by Django 4.2.13 on 2025-03-07 02:08

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('susaf_susoft', '0002_alter_project_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sprints', to='susaf_susoft.project')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('impact', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('social', 'Social'), ('individual', 'Individual'), ('environmental', 'Environmental'), ('economic', 'Economic'), ('technical', 'Technical')], max_length=20), blank=True, size=5)),
                ('type', models.CharField(choices=[('positive', 'Positive'), ('negative', 'Negative')], max_length=20)),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='susaf_susoft.sprint')),
            ],
        ),
        migrations.CreateModel(
            name='Metrics',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('done', 'Done'), ('in_progress', 'In Progress'), ('canceled', 'Canceled')], max_length=20)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='susaf_susoft.task')),
            ],
        ),
    ]
