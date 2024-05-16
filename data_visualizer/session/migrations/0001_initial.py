# Generated by Django 4.2.9 on 2024-04-16 21:40

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buildings',
            fields=[
                ('building_id', models.AutoField(primary_key=True, serialize=False)),
                ('pin', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='PIN must be in the format 00-00-000-000-0000.', regex='^\\d{2}-\\d{2}-\\d{3}-\\d{3}-\\d{4}$')])),
                ('address', models.CharField(max_length=100)),
                ('address_number', models.IntegerField()),
                ('address_street', models.CharField(max_length=100)),
                ('zip_code', models.IntegerField()),
                ('chicago_owned_property', models.BooleanField()),
                ('property_class', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator(message='Property class must be in the format 0-00.', regex='^\\d{1}-\\d{2}$')])),
                ('property_description', models.TextField()),
                ('tax_bill_2020', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax_bill_2021', models.DecimalField(decimal_places=2, max_digits=10)),
                ('assessment_2020', models.DecimalField(decimal_places=2, max_digits=10)),
                ('assessment_2021', models.DecimalField(decimal_places=2, max_digits=10)),
                ('units', models.IntegerField()),
                ('area_sq_ft', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lot_size_sf', models.DecimalField(decimal_places=2, max_digits=10)),
                ('property_tax_year', models.IntegerField()),
                ('taxpayer_name', models.CharField(max_length=100)),
                ('taxpayer_address', models.CharField(max_length=100)),
                ('taxpayer_city_state_zip', models.CharField(max_length=100)),
                ('time_last_checked', models.DateTimeField()),
            ],
            options={
                'db_table': 'buildings',
            },
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('business_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('dba', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('email', models.EmailField(max_length=100)),
                ('industry', models.CharField(max_length=100)),
                ('naics_code', models.CharField(max_length=6)),
                ('date_established', models.DateField(blank=True, default=datetime.datetime(2024, 4, 16, 21, 40, 52, 176745, tzinfo=datetime.timezone.utc), null=True)),
                ('legal_structure', models.CharField(max_length=100)),
                ('ein', models.CharField(max_length=9, validators=[django.core.validators.RegexValidator(message='EIN must be in the format 00-0000000.', regex='^\\d{2}-\\d{7}$')])),
                ('licenses', models.CharField()),
                ('status', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'businesses',
            },
        ),
        migrations.CreateModel(
            name='BusinessInitiativeProgram',
            fields=[
                ('bip_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('deliverables', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('contact', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'bips',
            },
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('client_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=100)),
                ('business_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='session.business')),
            ],
            options={
                'db_table': 'clients',
            },
        ),
        migrations.CreateModel(
            name='Consultant',
            fields=[
                ('consultant_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('specialty', models.CharField(choices=[('1', 'Capital Specialist'), ('2', 'Financial Specialist'), ('3', 'Licensing Specialist'), ('4', 'Cultural Specialist'), ('5', 'Technology Specialist'), ('6', 'Other')], max_length=2)),
                ('bip_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='session.businessinitiativeprogram')),
            ],
            options={
                'db_table': 'consultants',
            },
        ),
        migrations.CreateModel(
            name='Sessions',
            fields=[
                ('session_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='session.clients')),
                ('consultant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='session.consultant')),
            ],
            options={
                'db_table': 'advising_sessions',
            },
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('contact_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('business_role', models.CharField(max_length=100)),
                ('alt_phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('address', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField(default=datetime.datetime(2024, 4, 16, 21, 40, 52, 176088, tzinfo=datetime.timezone.utc))),
                ('gender', models.CharField(max_length=100)),
                ('ethnicity', models.CharField(max_length=100)),
                ('nationality', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=100)),
                ('registration_date', models.DateField(default=datetime.datetime(2024, 4, 16, 21, 40, 52, 176378, tzinfo=datetime.timezone.utc))),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='session.business')),
            ],
            options={
                'db_table': 'contacts',
            },
        ),
        migrations.AddField(
            model_name='clients',
            name='consultant_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='session.consultant'),
        ),
        migrations.AddField(
            model_name='clients',
            name='contact_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='session.contacts'),
        ),
        migrations.AddField(
            model_name='business',
            name='contact_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='session.contacts'),
        ),
        migrations.AddConstraint(
            model_name='buildings',
            constraint=models.UniqueConstraint(fields=('pin', 'address_number'), name='unique_building'),
        ),
        migrations.AddConstraint(
            model_name='contacts',
            constraint=models.CheckConstraint(check=models.Q(('date_of_birth__lte', datetime.date(2024, 4, 16))), name='valid_date_of_birth'),
        ),
        migrations.AddConstraint(
            model_name='contacts',
            constraint=models.CheckConstraint(check=models.Q(('gender__in', ['M', 'F', 'O', 'N'])), name='valid_gender_choice'),
        ),
        migrations.AddConstraint(
            model_name='contacts',
            constraint=models.CheckConstraint(check=models.Q(('registration_date__lte', datetime.date(2024, 4, 16))), name='valid_registration_date'),
        ),
        migrations.AddConstraint(
            model_name='consultant',
            constraint=models.CheckConstraint(check=models.Q(('specialty__in', ['1', '2', '3', '4', '5', '6'])), name='valid_specialty'),
        ),
        migrations.AddConstraint(
            model_name='clients',
            constraint=models.UniqueConstraint(fields=('business_id', 'contact_id'), name='unique_client'),
        ),
        migrations.AddConstraint(
            model_name='business',
            constraint=models.CheckConstraint(check=models.Q(('industry__in', ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'])), name='valid_industry'),
        ),
        migrations.AddConstraint(
            model_name='business',
            constraint=models.CheckConstraint(check=models.Q(('date_established__lte', datetime.date(2024, 4, 16))), name='valid_date_established'),
        ),
        migrations.AddConstraint(
            model_name='business',
            constraint=models.CheckConstraint(check=models.Q(('legal_structure__in', ['1', '2', '3', '4', '5', '6', '7', '8'])), name='valid_legal_structure'),
        ),
        migrations.AddConstraint(
            model_name='business',
            constraint=models.CheckConstraint(check=models.Q(('status__in', ['Active', 'Inactive', 'Closed'])), name='valid_status'),
        ),
    ]
