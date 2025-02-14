from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ui.models import Corpus, Document, Chunk, Keyword, Score

class BaseViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        self.corpus = Corpus.objects.create(
            name="Test Corpus",
            corpus_type="Type A",
            path="/path/to/corpus",
            username="user1",
            created_by=self.user
        )

        self.document = Document.objects.create(
            corpus=self.corpus,
            name="Test Document",
            title="Document Title",
            content="This is the content of the document.",
            description="This is a document description.",
            num_chunks=5,
            created_by=self.user
        )

        self.chunk = Chunk.objects.create(
            document=self.document,
            seq=1,
            chunk_txt="This is a test chunk.",
            start_index=0,
            end_index=100,
            vector={},
            chunk_size=128,
            created_by=self.user
        )

        self.keyword = Keyword.objects.create(
            word="test",
            short_desc="Short description",
            long_desc="Long description",
            created_by=self.user
        )

        self.score = Score.objects.create(
            chunk=self.chunk,
            keyword=self.keyword,
            value=0.95,
            created_by=self.user
        )

class TestCorpusViews(BaseViewTest):
    def test_corpus_list_view(self):
        url = reverse('corpus_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_object.html')
        self.assertEqual(response.context['object_type'], 'corpus')
        self.assertEqual(response.context['action'], 'list')
        self.assertIn('objects', response.context)
        self.assertEqual(len(response.context['objects']), 1)

    def test_corpus_create_view_get(self):
        url = reverse('create_corpus')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_object.html')
        self.assertEqual(response.context['object_type'], 'corpus')
        self.assertIn('form', response.context)

    def test_corpus_create_view_post(self):
        url = reverse('create_corpus')
        data = {
            'name': 'New Corpus',
            'corpus_type': 'Type B',
            'path': '/path/to/new',
            'username': 'testuser'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Corpus.objects.filter(name='New Corpus').exists())

    def test_corpus_edit_view_get(self):
        url = reverse('edit_corpus', args=[self.corpus.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_object.html')
        self.assertEqual(response.context['object_type'], 'corpus')
        self.assertIsNone(response.context.get('action'))
        self.assertIn('form', response.context)
        self.assertIn('object', response.context)

    def test_corpus_edit_view_post(self):
        url = reverse('edit_corpus', args=[self.corpus.id])
        data = {
            'name': 'Updated Corpus',
            'corpus_type': 'Type A',
            'path': '/path/to/corpus',
            'username': 'user1'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.corpus.refresh_from_db()
        self.assertEqual(self.corpus.name, 'Updated Corpus')

    def test_unauthenticated_access(self):
        self.client.logout()
        urls = [
            reverse('corpus_list'),
            reverse('create_corpus'),
            reverse('edit_corpus', args=[self.corpus.id])
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f'/login/?next={url}')

class TestDocumentViews(BaseViewTest):
    def test_document_list_view(self):
        url = reverse('document_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_object.html')
        self.assertEqual(response.context['object_type'], 'document')
        self.assertEqual(response.context['action'], 'list')
        self.assertIn('objects', response.context)
        self.assertEqual(len(response.context['objects']), 1)

    def test_document_create_view_get(self):
        url = reverse('create_document')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_object.html')
        self.assertEqual(response.context['object_type'], 'document')
        self.assertIsNone(response.context.get('action'))
        self.assertIn('form', response.context)

    def test_document_create_view_post(self):
        url = reverse('create_document')
        data = {
            'corpus': self.corpus.id,
            'name': 'New Document',
            'title': 'New Title',
            'content': 'New content.',
            'description': 'New description.',
            'num_chunks': 3
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Document.objects.filter(name='New Document').exists())

    def test_document_edit_view_get(self):
        url = reverse('edit_document', args=[self.document.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_object.html')
        self.assertEqual(response.context['object_type'], 'document')
        self.assertIsNone(response.context.get('action'))
        self.assertIn('form', response.context)
        self.assertIn('object', response.context)

    def test_document_edit_view_post(self):
        url = reverse('edit_document', args=[self.document.id])
        data = {
            'corpus': self.corpus.id,
            'name': 'Updated Document',
            'title': 'Updated Title',
            'content': 'Updated content.',
            'description': 'Updated description.',
            'num_chunks': 5
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.document.refresh_from_db()
        self.assertEqual(self.document.name, 'Updated Document')

    def test_unauthenticated_access(self):
        self.client.logout()
        urls = [
            reverse('document_list'),
            reverse('create_document'),
            reverse('edit_document', args=[self.document.id])
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f'/login/?next={url}')

class TestKeywordViews(BaseViewTest):
    def test_keyword_list_view(self):
        url = reverse('keyword_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_object.html')
        self.assertEqual(response.context['object_type'], 'keyword')
        self.assertEqual(response.context['action'], 'list')
        self.assertIn('objects', response.context)
        self.assertEqual(len(response.context['objects']), 1)

    def test_keyword_create_view_get(self):
        url = reverse('create_keyword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_object.html')
        self.assertEqual(response.context['object_type'], 'keyword')
        self.assertIsNone(response.context.get('action'))
        self.assertIn('form', response.context)

    def test_keyword_create_view_post(self):
        url = reverse('create_keyword')
        data = {
            'word': 'newkeyword',
            'short_desc': 'New short description',
            'long_desc': 'New long description'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Keyword.objects.filter(word='newkeyword').exists())

    def test_keyword_edit_view_get(self):
        url = reverse('edit_keyword', args=[self.keyword.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_object.html')
        self.assertEqual(response.context['object_type'], 'keyword')
        self.assertIsNone(response.context.get('action'))
        self.assertIn('form', response.context)
        self.assertIn('object', response.context)

    def test_keyword_edit_view_post(self):
        url = reverse('edit_keyword', args=[self.keyword.id])
        data = {
            'word': 'updatedkeyword',
            'short_desc': 'Updated short description',
            'long_desc': 'Updated long description'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.keyword.refresh_from_db()
        self.assertEqual(self.keyword.word, 'updatedkeyword')

    def test_unauthenticated_access(self):
        self.client.logout()
        urls = [
            reverse('keyword_list'),
            reverse('create_keyword'),
            reverse('edit_keyword', args=[self.keyword.id])
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f'/login/?next={url}')

class TestChunkViews(BaseViewTest):
    def test_chunk_list_view(self):
        url = reverse('chunk_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_object.html')
        self.assertEqual(response.context['object_type'], 'chunk')
        self.assertEqual(response.context['action'], 'list')
        self.assertIn('objects', response.context)
        self.assertEqual(len(response.context['objects']), 1)

    def test_chunk_create_view_get(self):
        url = reverse('create_chunk')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_object.html')
        self.assertEqual(response.context['object_type'], 'chunk')
        self.assertIsNone(response.context.get('action'))
        self.assertIn('form', response.context)

    def test_chunk_create_view_post(self):
        url = reverse('create_chunk')
        data = {
            'document': self.document.id,
            'seq': 2,
            'chunk_txt': 'New chunk text.',
            'start_index': 101,
            'end_index': 200,
            'vector': {},
            'chunk_size': 128
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Chunk.objects.filter(seq=2).exists())

    def test_chunk_edit_view_get(self):
        url = reverse('edit_chunk', args=[self.chunk.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_object.html')
        self.assertEqual(response.context['object_type'], 'chunk')
        self.assertIsNone(response.context.get('action'))
        self.assertIn('form', response.context)
        self.assertIn('object', response.context)

    def test_chunk_edit_view_post(self):
        url = reverse('edit_chunk', args=[self.chunk.id])
        data = {
            'document': self.document.id,
            'seq': 1,
            'chunk_txt': 'Updated chunk text.',
            'start_index': 0,
            'end_index': 100,
            'vector': {},
            'chunk_size': 128
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.chunk.refresh_from_db()
        self.assertEqual(self.chunk.chunk_txt, 'Updated chunk text.')

    def test_unauthenticated_access(self):
        self.client.logout()
        urls = [
            reverse('chunk_list'),
            reverse('create_chunk'),
            reverse('edit_chunk', args=[self.chunk.id])
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f'/login/?next={url}')

class TestScoreViews(BaseViewTest):
    def test_score_list_view(self):
        url = reverse('score_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_object.html')
        self.assertEqual(response.context['object_type'], 'score')
        self.assertEqual(response.context['action'], 'list')
        self.assertIn('objects', response.context)
        self.assertEqual(len(response.context['objects']), 1)

    def test_score_create_view_get(self):
        url = reverse('create_score')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_object.html')
        self.assertEqual(response.context['object_type'], 'score')
        self.assertIsNone(response.context.get('action'))
        self.assertIn('form', response.context)

    def test_score_create_view_post(self):
        url = reverse('create_score')
        data = {
            'chunk': self.chunk.id,
            'keyword': self.keyword.id,
            'value': 0.85
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Score.objects.filter(value=0.85).exists())

    def test_score_edit_view_get(self):
        url = reverse('edit_score', args=[self.score.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_object.html')
        self.assertEqual(response.context['object_type'], 'score')
        self.assertIsNone(response.context.get('action'))
        self.assertIn('form', response.context)
        self.assertIn('object', response.context)

    def test_score_edit_view_post(self):
        url = reverse('edit_score', args=[self.score.id])
        data = {
            'chunk': self.chunk.id,
            'keyword': self.keyword.id,
            'value': 0.90
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.score.refresh_from_db()
        self.assertEqual(self.score.value, 0.90)

    def test_unauthenticated_access(self):
        self.client.logout()
        urls = [
            reverse('score_list'),
            reverse('create_score'),
            reverse('edit_score', args=[self.score.id])
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f'/login/?next={url}')
