# Generated by Django 4.2.9 on 2024-09-06 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0016_remove_business_valid_date_established_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='licenses',
            field=models.CharField(max_length=100),
        ),
    ]
