''' This file contains the tests for the models in the ui app.'''
from django.test import TestCase
from django.contrib.auth.models import User
from ui.models import Corpus, Document, Chunk, Keyword, Score

class ModelTests(TestCase):
    '''Test the models'''

    def setUp(self):
        '''Set up the test data'''
        self.user = User.objects.create_user(username='testuser', password='12345')

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

    def test_corpus_creation(self):
        '''Test corpus creation'''
        self.assertEqual(self.corpus.name, "Test Corpus")
        self.assertEqual(self.corpus.corpus_type, "Type A")
        self.assertEqual(self.corpus.path, "/path/to/corpus")
        self.assertEqual(self.corpus.username, "user1")
        self.assertEqual(self.corpus.created_by, self.user)

    def test_document_creation(self):
        '''Test document creation'''
        self.assertEqual(self.document.name, "Test Document")
        self.assertEqual(self.document.title, "Document Title")
        self.assertEqual(self.document.content, "This is the content of the document.")
        self.assertEqual(self.document.description, "This is a document description.")
        self.assertEqual(self.document.num_chunks, 5)
        self.assertEqual(self.document.corpus, self.corpus)
        self.assertEqual(self.document.created_by, self.user)

    def test_chunk_creation(self):
        '''Test chunk creation'''
        self.assertEqual(self.chunk.document, self.document)
        self.assertEqual(self.chunk.seq, 1)
        self.assertEqual(self.chunk.chunk_txt, "This is a test chunk.")
        self.assertEqual(self.chunk.start_index, 0)
        self.assertEqual(self.chunk.end_index, 100)
        self.assertEqual(self.chunk.vector, {})
        self.assertEqual(self.chunk.chunk_size, 128)
        self.assertEqual(self.chunk.created_by, self.user)

    def test_keyword_creation(self):
        '''Test keyword creation'''
        self.assertEqual(self.keyword.word, "test")
        self.assertEqual(self.keyword.short_desc, "Short description")
        self.assertEqual(self.keyword.long_desc, "Long description")
        self.assertEqual(self.keyword.created_by, self.user)

    def test_score_creation(self):
        '''Test score creation'''
        self.assertEqual(self.score.chunk, self.chunk)
        self.assertEqual(self.score.keyword, self.keyword)
        self.assertEqual(self.score.value, 0.95)
        self.assertEqual(self.score.created_by, self.user)
