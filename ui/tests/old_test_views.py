import pytest
from django.test import TestCase, Client
from django.urls import reverse
from ui.models import Corpus, Keyword

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.corpus = Corpus.objects.create(
            name="Test Corpus",
            type="Type A",
            path="/path/to/corpus",
            username="user1",
            ingest_at="2025-01-01T00:00:00Z"
        )
        self.keyword = Keyword.objects.create(
            word="test",
            short_desc="Short description",
            long_desc="Long description",
            created_at="2025-01-01T00:00:00Z"
        )

    def test_manage_corpus_get(self):
        response = self.client.get(reverse('manage_corpus'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_corpus.html')
        self.assertIn('corpora', response.context)
        self.assertFalse(response.context['show_form'])

    def test_manage_corpus_post(self):
        response = self.client.post(reverse('manage_corpus'), {
            'name': 'New Corpus',
            'type': 'Type B',
            'path': '/path/to/new_corpus',
            'username': 'user2',
            'ingest_at': '2025-02-01T00:00:00Z'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Corpus.objects.count(), 2)

    def test_corpus_list(self):
        response = self.client.get(reverse('corpus_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'corpus_list.html')
        self.assertIn('corpora', response.context)

    def test_create_corpus_get(self):
        response = self.client.get(reverse('create_corpus'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_corpus.html')

    def test_create_corpus_post(self):
        response = self.client.post(reverse('create_corpus'), {
            'name': 'Another Corpus',
            'type': 'Type C',
            'path': '/another/path',
            'username': 'user3',
            'ingest_at': '2025-03-01T00:00:00Z'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Corpus.objects.count(), 2)

    def test_manage_keywords_get(self):
        response = self.client.get(reverse('manage_keywords'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_keywords.html')
        self.assertIn('keywords', response.context)
        self.assertFalse(response.context['show_form'])

    def test_manage_keywords_post(self):
        response = self.client.post(reverse('manage_keywords'), {
            'word': 'new_word',
            'short_desc': 'Short desc',
            'long_desc': 'Long desc',
            'created_at': '2026-01-01T00:00:00Z'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Keyword.objects.count(), 2)

    def test_keyword_list(self):
        response = self.client.get(reverse('keyword_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'keyword_list.html')
        self.assertIn('keywords', response.context)

    def test_create_keyword_get(self):
        response = self.client.get(reverse('create_keyword'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_keyword.html')

    def test_create_keyword_post(self):
        response = self.client.post(reverse('create_keyword'), {
            'word': 'another_word',
            'short_desc': 'Another short desc',
            'long_desc': 'Another long desc',
            'created_at': '2026-02-01T00:00:00Z'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Keyword.objects.count(), 2)
