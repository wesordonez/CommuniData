# Generated by Django 4.2.9 on 2024-04-17 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0013_remove_sessions_valid_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sessions',
            name='duration',
        ),
    ]
