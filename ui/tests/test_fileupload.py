import os
from django.core.files.uploadedfile import SimpleUploadedFile
from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ui.models import Corpus, Document, Chunk
import pandas as pd

class FileUploadTests(TestCase):
    '''Test file upload functionality'''

    def setUp(self):
        '''Set up the test data'''
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Create a sample Excel file for testing
        self.test_file_path = 'testfile.xlsx'
        df = pd.DataFrame({
            'Column1': ['Value1', 'Value2'],
            'Column2': ['Value3', 'Value4']
        })
        df.to_excel(self.test_file_path, index=False)

    def tearDown(self):
        '''Clean up the test data'''
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_upload_corpus(self):
        '''Test uploading a corpus'''
        url = reverse('upload_corpus')
        print(f"URL: {url}")  # Debug print

        with open(self.test_file_path, 'rb') as f:
            data = {
                'name': 'Test Corpus',
                'corpus_type': 'Type A',
                'username': 'testuser',
                'file': f
            }
            print(f"Data keys: {data.keys()}")  # Debug print
            response = self.client.post(url, data)  # Remove format parameter

        print(f"Response: {response.status_code}")  # Debug print
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Corpus.objects.filter(name='Test Corpus').exists())

    def test_upload_duplicate_corpus(self):
        url = reverse('upload_corpus')
        data = {
            'name': 'Test Corpus',
            'type': 'Test Type',
            'username': 'testuser'
        }

        # First upload
        with open(self.test_file_path, 'rb') as file:
            data['file'] = file
            response = self.client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, HTTPStatus.CREATED)

        # Attempt to upload the same corpus again
        with open(self.test_file_path, 'rb') as file:
            data['file'] = file
            response = self.client.post(url, data, format='multipart')
            print(response.content)  # Debugging line
            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
            self.assertEqual(response.data['error'], 'Corpus already exists.')
