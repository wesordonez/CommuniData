# Generated by Django 4.2.9 on 2024-04-16 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0004_alter_business_contact_id_alter_contacts_business_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='notes',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='business',
            name='num_employees',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='business',
            name='website',
            field=models.URLField(default=' '),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contacts',
            name='notes',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
    ]
