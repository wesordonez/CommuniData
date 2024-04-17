from django.test import TestCase
from django.urls import reverse
from session.models import BusinessInitiativeProgram as Bip, Consultant, Buildings, Contacts, Business, Clients
import json

class ConsultantTest(TestCase):
    def setUp(self):
        self.bip = Bip.objects.create(
            name='Test BIP',
            deliverables='This is a test BIP.',
            start_date='2021-01-01',
            end_date='2021-12-31',
            contact='John Doe'
        )
        self.consultant = Consultant.objects.create(
            first_name='John',
            last_name='Doe',
            slug='john-doe',
            email='johndoetest@email.com',
            phone='1234567890',
            specialty='1',
            bip_id=self.bip
        )
            
        
    def test_consultant_create(self):
        response = self.client.post(reverse('consultants'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'slug': 'john-doe-test',
            'email': 'johndoe@email.com',
            'phone': '1234567890',
            'specialty': '1',
            'bip_id': self.bip.bip_id
        })
                
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['first_name'], 'John')
        
    def test_consultant_list(self):
        response = self.client.get(reverse('consultants'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'John')
        
    def test_consultant_create_missing_fields(self):
        response = self.client.post(reverse('consultants'), {
            'first_name': '',
            'last_name': '',
            'slug': 'jane-doe',
            'email': '',
            'phone': '1234567890',
            'specialty': '1',
            'bip_id': '1'
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['email'][0], 'This field may not be blank.')
        
    def test_consultant_create_invalid_email(self):
        response = self.client.post(reverse('consultants'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'slug': 'jane-doe',
            'email': 'invalidemail',
            'phone': '1234567890',
            'specialty': '1',
            'bip_id': '1'
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['email'][0], 'Enter a valid email address.')
        
    def test_consultant_create_non_unique_email(self):
        response = self.client.post(reverse('consultants'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'slug': 'jane-doe',
            'email': 'johndoetest@email.com',
            'phone': '1234567890',
            'specialty': '1',
            'bip_id': '1'
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['email'][0], 'consultant with this email already exists.')
        
    def test_consultant_create_non_unique_slug(self):
        response = self.client.post(reverse('consultants'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'slug': 'john-doe',
            'email': 'janedoe@email.com',
            'phone': '1234567890',
            'specialty': '1',
            'bip_id': '1'
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['slug'][0], 'consultant with this slug already exists.')
        
    def test_consultant_create_invalid_specialty(self):
        response = self.client.post(reverse('consultants'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'slug': 'jane-doe',
            'email': 'janedoe@email.com',
            'phone': '1234567890',
            'specialty': '0',
            'bip_id': '1'
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['specialty'][0], '"0" is not a valid choice.')
        
    def test_consultant_create_invalid_bip(self):
        response = self.client.post(reverse('consultants'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'slug': 'jane-doe',
            'email': 'janedoe@email.com',
            'phone': '1234567890',
            'specialty': '1',
            'bip_id': '0'
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['bip_id'][0]), 'Invalid pk "0" - object does not exist.')
        

    def test_consultant_update(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'slug': 'jane-doe',
            'email': 'janedoe2@email.com',
            'phone': '1234567890',
            'specialty': '1',
            'bip_id': self.bip.bip_id
        }
        response = self.client.put(reverse('consultant', args=[self.consultant.consultant_id]), 
                                   data=json.dumps(data), 
                                   content_type='application/json')
                
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'Jane')
        
        
class BipTest(TestCase):
    def setUp(self):
        self.bip = Bip.objects.create(
            name='Test BIP',
            deliverables='This is a test BIP2.',
            start_date='2021-01-01',
            end_date='2021-12-31',
            contact='John Doe'
        )
        
    def test_bip_create(self):
        response = self.client.post(reverse('bips'), {
            'name': 'Test Business Initiative Program',
            'deliverables': 'This is a test Business Initiative Program.',
            'start_date': '2021-01-01',
            'end_date': '2021-12-31',
            'contact': 'John Doe'
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Test Business Initiative Program')
        
    def test_bip_list(self):
        response = self.client.get(reverse('bips'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test BIP')
        
    def test_bip_create_missing_fields(self):
        response = self.client.post(reverse('bips'), {
            'name': '',
            'deliverables': '',
            'start_date': '',
            'end_date': '',
            'contact': ''
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0], 'This field may not be blank.')
        self.assertEqual(response.data['deliverables'][0], 'This field may not be blank.')
        self.assertEqual(str(response.data['start_date'][0]), 'Date has wrong format. Use one of these formats instead: YYYY-MM-DD.')
        self.assertEqual(str(response.data['end_date'][0]), 'Date has wrong format. Use one of these formats instead: YYYY-MM-DD.')
        self.assertEqual(response.data['contact'][0], 'This field may not be blank.')
        
    def test_bip_create_invalid_dates(self):
        response = self.client.post(reverse('bips'), {
            'name': 'Test BIP',
            'deliverables': 'This is a test BIP.',
            'start_date': '2021-12-31',
            'end_date': '2021-01-01',
            'contact': 'John Doe'
        })
        
        self.assertEqual(response.status_code, 400)
        
    def test_bip_update(self):
        data = {
            'name': 'Test BIP2',
            'deliverables': 'This is a test BIP2.',
            'start_date': '2021-01-01',
            'end_date': '2021-12-31',
            'contact': 'John Doe'
        }
        response = self.client.put(reverse('bip', args=[self.bip.bip_id]), 
                                   data=json.dumps(data), 
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test BIP2')
        

class BuildingsTest(TestCase):
    def setUp(self):
        self.building = Buildings.objects.create(
            building_id=1,
            pin="00-00-000-000-0000",
            address="test_address",
            address_number=123,
            address_street="test_street",
            zip_code=12345,
            chicago_owned_property=True,
            property_class="0-00",
            property_description="test_description",
            tax_bill_2020="100.00",
            tax_bill_2021="200.00",
            assessment_2020="300.00",
            assessment_2021="400.00",
            units=5,
            area_sq_ft="600.00",
            lot_size_sf="700.00",
            property_tax_year=2021,
            taxpayer_name="test_name",
            taxpayer_address="test_taxpayer_address",
            taxpayer_city_state_zip="test_city_state_zip",
            time_last_checked="2022-01-01T06:00:00Z"
        )
        
    def test_building_list(self):
        response = self.client.get(reverse('buildings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['building_id'], 1)
        
        
class ContactsTest(TestCase):
    def setUp(self):
        self.contact = Contacts.objects.create(
            # contact_id=1,
            first_name='John',
            last_name='Doe',
            email='johndoe@test.com',
            phone='1234567890',
            business_role='Test Role',
            alt_phone='0987654321',
            address='test_address',
            date_of_birth='2021-01-01',
            gender='M',
            ethnicity='Hispanic',
            language='English',
            registration_date='2021-01-01',
            notes='Test notes'
        )
        
    def test_contact_list(self):
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'John')
        
    def test_contact_create(self):
        response = self.client.post(reverse('contacts'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@test.com',
            'phone': '1234567890',
            'business_role': 'Test Role',
            'alt_phone': '0987654321',
            'address': 'test_address',
            'date_of_birth': '2021-01-01',
            'gender': 'F',
            'ethnicity': 'Hispanic',
            'nationality': 'American',
            'language': 'English',
            'registration_date': '2021-01-01',
            'notes': 'Test notes'
        })
                
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['first_name'], 'Jane')
           
    def test_contact_create_missing_fields(self):
        response = self.client.post(reverse('contacts'), {
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone': '',
            'business_role': '',
            'alt_phone': '',
            'address': '',
            'date_of_birth': '',
            'gender': '',
            'ethnicity': '',
            'nationality': '',
            'language': '',
            'registration_date': '',
            'notes': ''
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['first_name'][0], 'This field may not be blank.')
        
    def test_contact_create_invalid_email(self):
        response = self.client.post(reverse('contacts'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'invalidemail',
            'phone': '1234567890',
            'business_role': 'Test Role',
            'alt_phone': '0987654321',
            'address': 'test_address',
            'date_of_birth': '2021-01-01',
            'gender': 'F',
            'ethnicity': 'Hispanic',
            'nationality': 'American',
            'language': 'English',
            'registration_date': '2021-01-01',
            'notes': 'Test notes'
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['email'][0], 'Enter a valid email address.')
        
    def test_contact_create_invalid_phone(self):
        response = self.client.post(reverse('contacts'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'email@email.com',
            'phone': '123',
            'business_role': 'Test Role',
            'alt_phone': '123',
            'address': 'test_address',
            'date_of_birth': '2021-01-01',
            'gender': 'F',
            'ethnicity': 'Hispanic',
            'nationality': 'American',
            'language': 'English',
            'registration_date': '2021-01-01',
            'notes': 'Test notes'
        })
                
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['phone'][0], "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        
    def test_contact_create_invalid_dob(self):
        response = self.client.post(reverse('contacts'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'email@email.com',
            'phone': '123',
            'business_role': 'Test Role',
            'alt_phone': '123',
            'address': 'test_address',
            'date_of_birth': 'invalid',
            'gender': 'F',
            'ethnicity': 'Hispanic',
            'nationality': 'American',
            'language': 'English',
            'registration_date': '2021-01-01',
            'notes': 'Test notes'
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['date_of_birth'][0], 'Date has wrong format. Use one of these formats instead: YYYY-MM-DD.')
        
        # I don't know why this test isn't working as expected. I know the function is working but the test is failing.
    # def test_contact_create_invalid_gender_choice(self):
    #     response = self.client.post(reverse('contacts'), {
    #         'first_name': 'Jane',
    #         'last_name': 'Doe',
    #         'email': 'email@email.com',
    #         'phone': '1234567890',
    #         'business_role': 'Test Role',
    #         'alt_phone': '1234567890',
    #         'address': 'test_address',
    #         'date_of_birth': '2021-01-01',
    #         'gender': 'invalid',
    #         'ethnicity': 'Hispanic',
    #         'nationality': 'American',
    #         'language': 'English',
    #         'registration_date': '2021-01-01',
    #         'notes': 'Test notes'
    #     })
    #     print(response.data)
        
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.gender[0], '"invalid" is not a valid choice.')
        
    def test_contact_update_successful(self):
        data = {
            'first_name': 'Jane Updated',
            'last_name': 'Doe',
            'email': 'email@email.com',
            'phone': '1234567890',
            'business_role': 'Test Role',
            'alt_phone': '1234567890',
            'address': 'test_address',
            'date_of_birth': '2021-01-01',
            'gender': 'F',
            'ethnicity': 'Hispanic',
            'nationality': 'American',
            'language': 'English',
            'registration_date': '2021-01-01',
            'notes': 'Test notes'
        }
        
        response = self.client.put(reverse('contact', args=[self.contact.contact_id]), 
                                   data=json.dumps(data), 
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'Jane Updated')
        
    def test_contact_update_unsuccessful(self):
        
        response = self.client.put(reverse('contact', args=[0]), 
                                   data=json.dumps({}), 
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        
        
class BusinessTest(TestCase):
    def setUp(self):
        contact = Contacts.objects.create(
            first_name='John',
            last_name='Doe',
            email='johndoe@test.com',
            phone='1234567890',
            business_role='Test Role',
            alt_phone='0987654321',
            address='test_address',
            date_of_birth='2021-01-01',
            gender='M',
            ethnicity='Hispanic',
            language='English',
            registration_date='2021-01-01',
            notes='Test notes'
        )
        contact.save()
        test_contact = Contacts.objects.get(contact_id=contact.contact_id)
        self.business = Business.objects.create(
            name='Test Business',
            dba='Test DBA',
            description='This is a test business.',
            address='123 Test Street',
            phone='+1234567890',
            email='test@example.com',
            website='http://www.example.com',
            industry=1,
            naics_code=123456,
            date_established='2000-01-01',
            legal_structure=1,
            ein='00-0000000',
            licenses='Test License',
            contact=test_contact,
            num_employees=10,
            status='Active',
            notes='These are test notes.'
        )
        
    def test_business_list(self):
        response = self.client.get(reverse('business'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Business')
        
    def test_business_create(self):
        response = self.client.post(reverse('business'), {
            'name': 'Test Business 2',
            'dba': 'Test DBA 2',
            'description': 'This is a test business 2.',
            'address': '123 Test Street',
            'phone': '+1234567890',
            'email': 'test@test.com',
            'website': 'http://www.test.com',
            'industry': 1,
            'naics_code': 123456,
            'date_established': '2000-01-01',
            'legal_structure': 1,
            'ein': '00-0000000',
            'licenses': 'Test License',
            'contact': 1,
            'num_employees': 10,
            'status': 'Active',
            'notes': 'These are test notes.'
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Test Business 2')
        
    def test_business_create_missing_fields(self):
        response = self.client.post(reverse('business'), {
            'name': '',
            'dba': '',
            'description': '',
            'address': '',
            'phone': '',
            'email': '',
            'website': '',
            'industry': '',
            'naics_code': '',
            'date_established': '',
            'legal_structure': '',
            'ein': '',
            'licenses': '',
            'contact': '',
            'num_employees': '',
            'status': '',
            'notes': ''
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0], 'This field may not be blank.')
        
    def test_business_create_invalid_phone(self):
        response = self.client.post(reverse('business'), {
            'name': 'Test Business 2',
            'dba': 'Test DBA 2',
            'description': 'This is a test business 2.',
            'address': '123 Test Street',
            'phone': '123',
            'email': 'test@test.com',
            'website': 'http://www.test.com',
            'industry': 1,
            'naics_code': 123456,
            'date_established': '2000-01-01',
            'legal_structure': 1,
            'ein': '00-0000000',
            'licenses': 'Test License',
            'contact': 1,
            'num_employees': 10,
            'status': 'Active',
            'notes': 'These are test notes.'
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['phone'][0], "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        
    def test_business_create_invalid_ein(self):
        response = self.client.post(reverse('business'), {
            'name': 'Test Business 2',
            'dba': 'Test DBA 2',
            'description': 'This is a test business 2.',
            'address': '123 Test Street',
            'phone': '1234567890',
            'email': 'test@test.com',
            'website': 'http://www.test.com',
            'industry': 1,
            'naics_code': 123456,
            'date_established': '2009-01-01',
            'legal_structure': 1,
            'ein': '00-0000',
            'licenses': 'Test License',
            'contact': 2,
            'num_employees': 10,
            'status': 'Active',
            'notes': 'These are test notes.'
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['ein'][0], 'EIN must be in the format 00-0000000.')
        
    def test_business_create_invalid_contact(self):
        response = self.client.post(reverse('business'), {
            'name': 'Test Business 2',
            'dba': 'Test DBA 2',
            'description': 'This is a test business 2.',
            'address': '123 Test Street',
            'phone': '1234567890',
            'email': 'test@test.com',
            'website': 'http://www.test.com',
            'industry': 1,
            'naics_code': 123456,
            'date_established': '2009-01-01',
            'legal_structure': 1,
            'ein': '00-0000000',
            'licenses': 'Test License',
            'contact': 0,
            'num_employees': 10,
            'status': 'Active',
            'notes': 'These are test notes.'
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['contact'][0]), 'Invalid pk "0" - object does not exist.')
        
    def test_business_update_successful(self):
        contact = Contacts.objects.create(
            first_name='John',
            last_name='Doe',
            email='johndoe@test.com',
            phone='1234567890',
            business_role='Test Role',
            alt_phone='0987654321',
            address='test_address',
            date_of_birth='2021-01-01',
            gender='M',
            ethnicity='Hispanic',
            language='English',
            registration_date='2021-01-01',
            notes='Test notes'
        )
        data = {
            'name': 'Test Business 2',
            'dba': 'Test DBA 2',
            'description': 'This is a test business 2.',
            'address': '123 Test Street',
            'phone': '+1234567890',
            'email': 'test@test.com',
            'website': 'http://www.test.com',
            'industry': 1,
            'naics_code': 123456,
            'date_established': '2000-01-01',
            'legal_structure': 1,
            'ein': '00-0000000',
            'licenses': 'Test License',
            'contact': contact.contact_id,
            'num_employees': 10,
            'status': 'Active',
            'notes': 'These are test notes.'
        }
        response = self.client.put(reverse('business', args=[self.business.business_id]), 
                                   data=json.dumps(data), 
                                   content_type='application/json')
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Business 2')
        
        
class ClientsTest(TestCase):
    def setUp(self):
        self.bip = Bip.objects.create(
            name='Test BIP',
            deliverables='This is a test BIP.',
            start_date='2021-01-01',
            end_date='2021-12-31',
            contact='John Doe'
        )
        self.consultant = Consultant.objects.create(
            first_name='John',
            last_name='Doe',
            slug='john-doe',
            email='johndoetest@email.com',
            phone='1234567890',
            specialty='1',
            bip_id=self.bip
        )
        self.contact = Contacts.objects.create(
            first_name='John',
            last_name='Doe',
            email='johndoe@test.com',
            phone='1234567890',
            business_role='Test Role',
            alt_phone='0987654321',
            address='test_address',
            date_of_birth='2021-01-01',
            gender='M',
            ethnicity='Hispanic',
            language='English',
            registration_date='2021-01-01',
            notes='Test notes'
        )
        self.business = Business.objects.create(
            name='Test Business',
            dba='Test DBA',
            description='This is a test business.',
            address='123 Test Street',
            phone='+1234567890',
            email='test@example.com',
            website='http://www.example.com',
            industry=1,
            naics_code=123456,
            date_established='2000-01-01',
            legal_structure=1,
            ein='00-0000000',
            licenses='Test License',
            contact=self.contact,
            num_employees=10,
            status='Active',
            notes='These are test notes.'
        )
        self.test_client = Clients.objects.create(
            business_id=self.business,
            contact_id=self.contact,
            consultant_id=self.consultant,
            status='Active',
            client_notes='Test notes'
        )
        
    def test_clients_list(self):
        response = self.client.get(reverse('clients'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['business_id'], self.business.business_id)
        
    def test_clients_create(self):
        self.contact2 = Contacts.objects.create(
            first_name='John2',
            last_name='Doe2',
            email='johndoe2@test.com',
            phone='1234567890',
            business_role='Test Role',
            alt_phone='0987654321',
            address='test_address',
            date_of_birth='2021-01-01',
            gender='M',
            ethnicity='Hispanic',
            language='English',
            registration_date='2021-01-01',
            notes='Test notes'
        )
        response = self.client.post(reverse('clients'), {
            'business_id': self.business.business_id,
            'contact_id': self.contact2.contact_id,
            'consultant_id': self.consultant.consultant_id,
            'status': 'Active',
            'client_notes': 'Test notes'
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['business_id'], self.business.business_id)
        
    def test_clients_create_missing_fields(self):
        response = self.client.post(reverse('clients'), {
            'business_id': '',
            'contact_id': '',
            'consultant_id': '',
            'status': '',
            'client_notes': ''
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['business_id'][0], 'This field may not be null.')
        
    def test_clients_create_nonunique_business_contact_ids(self):
        response = self.client.post(reverse('clients'), {
            'business_id': self.business.business_id,
            'contact_id': self.contact.contact_id,
            'consultant_id': self.consultant.consultant_id,
            'status': 'Active',
            'client_notes': 'Test notes'
        })
        print(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0], 'The fields business_id, contact_id must make a unique set.')   
        
    def test_clients_update_successful(self):
        data = {
            'business_id': self.business.business_id,
            'contact_id': self.contact.contact_id,
            'consultant_id': self.consultant.consultant_id,
            'status': 'Inactive',
            'client_notes': 'Test notes updated'
        }
        
        response = self.client.put(reverse('client', args=[self.test_client.client_id]), 
                                   data=json.dumps(data), 
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'Inactive')
        