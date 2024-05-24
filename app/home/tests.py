from django.test import TestCase
from django.urls import reverse


class ContactSubmissionTest(TestCase):
    def test_contact_submission_success(self):
        # Make a POST request to the contact submission endpoint
        response = self.client.post(reverse('contact'), {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'message': 'Hello, this is a test message.'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        
    def test_contact_submission_missing_fields(self):
        # Make a POST request to the contact submission endpoint with missing fields
        response = self.client.post(reverse('contact'), {
            'name': '',
            'email': 'johndoe@example.com',
            'message': 'Hello, this is a test message.'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')
        
    def test_contact_submission_invalid_email(self):
        # Make a POST request to the contact submission endpoint with an invalid email
        response = self.client.post(reverse('contact'), {
            'name': 'John Doe',
            'email': 'invalidemail',
            'message': 'Hello, this is a test message.'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid email address.')
    
    def test_contact_submission_non_unique_email_phone(self):
    # Make a POST request to the contact submission endpoint with a non-unique email and phone
        test1 = self.client.post(reverse('contact'), {
            'name': 'John Doe',
            'email': 'email@email.com',
            'phone': '1234567890',
            'message': 'Hello, this is a test message.'
        })
        response = self.client.post(reverse('contact'), {
            'name': 'Jane Doe',
            'email': 'email@email.com',
            'phone': '1234567890',
            'message': 'Hello, this is a test message.'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact submission with this Email and Phone already exists.')
        