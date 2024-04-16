from django.test import TestCase
from django.urls import reverse
from session.models import BusinessInitiativeProgram as Bip
from session.models import Consultant
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
        
