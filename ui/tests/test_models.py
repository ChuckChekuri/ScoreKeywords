''' This file contains the tests for the models in the ui app.'''
from django.test import TestCase
from ui.models import Corpus, Document, Chunk, Keyword, Score
from ui.models import KeywordReport, DocumentReport, CorpusReport

#pylint: disable=E1101
class ModelTests(TestCase):
    '''Test the models'''

    def setUp(self):
        '''Set up the test data'''
        self.corpus = Corpus.objects.create(
            name="Test Corpus",
            type="Type A",
            path="/path/to/corpus",
            username="user1"
        )
        self.document = Document.objects.create(
            corpus=self.corpus,
            name="Test document.",
            description="This is document description.",
            num_chunks=5,
            created_at="2025-02-01T00:00:00Z"
        )
        self.chunk = Chunk.objects.create(
            document=self.document,
            seq=1,
            chunk_txt="This is a test chunk.",
            vector=[0.1, 0.2, 0.3],
            chunk_size=100
        )
        self.keyword = Keyword.objects.create(
            word="test",
            short_desc="Short description",
            long_desc="Long description"
        )

    def test_create_corpus(self):
        '''Test creating a corpus'''
        corpus = Corpus.objects.create(
            name="Another Corpus",
            type="Type B",
            path="/path/to/another_corpus",
            username="user2"
        )
        self.assertEqual(corpus.name, "Another Corpus")
        self.assertEqual(corpus.type, "Type B")
        self.assertEqual(corpus.path, "/path/to/another_corpus")
        self.assertEqual(corpus.username, "user2")
        self.assertEqual(corpus.ingest_at, corpus.ingest_at)

    def test_create_document(self):
        '''Test creating a document'''
        document = Document.objects.create(
            corpus=self.corpus,
            name="Test document.",
            description="This is document description.",
            num_chunks=5,
            created_at="2025-02-01T00:00:00Z"
        )
        self.assertEqual(document.name, "Test document.")
        self.assertEqual(document.description, "This is document description.")
        self.assertEqual(document.num_chunks, 5)
        self.assertEqual(document.corpus, self.corpus)

    def test_create_chunk(self):
        '''Test creating a chunk'''
        chunk = Chunk.objects.create(
            document=self.document,
            seq=2,
            chunk_txt="This is another test chunk.",
            vector=[0.4, 0.5, 0.6],
            chunk_size=200
        )
        self.assertEqual(chunk.seq, 2)
        self.assertEqual(chunk.chunk_txt, "This is another test chunk.")
        self.assertEqual(chunk.vector, [0.4, 0.5, 0.6])
        self.assertEqual(chunk.chunk_size, 200)
        self.assertEqual(chunk.document, self.document)

    def test_create_keyword(self):
        '''Test creating a keyword'''
        keyword = Keyword.objects.create(
            word="another_test",
            short_desc="Another short description",
            long_desc="Another long description"
        )
        self.assertEqual(keyword.word, "another_test")
        self.assertEqual(keyword.short_desc, "Another short description")
        self.assertEqual(keyword.long_desc, "Another long description")

    def test_create_score(self):
        '''Test creating a score'''
        score = Score.objects.create(
            keyword=self.keyword,
            chunk=self.chunk,
            score=0.95
        )
        self.assertEqual(score.score, 0.95)
        self.assertEqual(score.keyword, self.keyword)
        self.assertEqual(score.chunk, self.chunk)

    def test_create_keyword_report(self):
        '''Test creating a keyword report'''
        keyword_report = KeywordReport.objects.create(
            keyword=self.keyword,
            title="Test Keyword Report",
            type="Summary",
            scores=[0.8, 0.9],
            summary="This is a test keyword report summary.",
            report="This is a test keyword report.",
            review="This is a test review.",
            reviewer="Reviewer 1"
        )
        self.assertEqual(keyword_report.title, "Test Keyword Report")
        self.assertEqual(keyword_report.type, "Summary")
        self.assertEqual(keyword_report.scores, [0.8, 0.9])
        self.assertEqual(keyword_report.summary, "This is a test keyword report summary.")
        self.assertEqual(keyword_report.report, "This is a test keyword report.")
        self.assertEqual(keyword_report.review, "This is a test review.")
        self.assertEqual(keyword_report.reviewer, "Reviewer 1")
        self.assertEqual(keyword_report.keyword, self.keyword)

    def test_create_document_report(self):
        '''Test creating a document report'''
        document_report = DocumentReport.objects.create(
            document=self.document,
            type="Summary",
            title="Test Document Report",
            scores=[0.7, 0.85],
            desc="This is a test document report description.",
            summary="This is a test document report summary.",
            report="This is a test document report.",
            review="This is a test review.",
            reviewer="Reviewer1"
        )
        self.assertEqual(document_report.title, "Test Document Report")
        self.assertEqual(document_report.type, "Summary")
        self.assertEqual(document_report.scores, [0.7, 0.85])
        self.assertEqual(document_report.desc, "This is a test document report description.")
        self.assertEqual(document_report.summary, "This is a test document report summary.")
        self.assertEqual(document_report.report, "This is a test document report.")
        self.assertEqual(document_report.review, "This is a test review.")
        self.assertEqual(document_report.reviewer, "Reviewer1")
        self.assertEqual(document_report.document, self.document)

    def test_create_corpus_report(self):
        '''Test creating a corpus report'''
        corpus_report = CorpusReport.objects.create(
            corpus=self.corpus,
            type="Summary",
            title="Test Corpus Report",
            desc="This is a test corpus report description.",
            summary="This is a test corpus report summary.",
            scores=[0.75, 0.85],
            report="This is a test corpus report.",
            review="This is a test review.",
            reviewer="Reviewer2"
        )
        self.assertEqual(corpus_report.title, "Test Corpus Report")
        self.assertEqual(corpus_report.type, "Summary")
        self.assertEqual(corpus_report.desc, "This is a test corpus report description.")
        self.assertEqual(corpus_report.summary, "This is a test corpus report summary.")
        self.assertEqual(corpus_report.scores, [0.75, 0.85])
        self.assertEqual(corpus_report.report, "This is a test corpus report.")
        self.assertEqual(corpus_report.review, "This is a test review.")
        self.assertEqual(corpus_report.reviewer, "Reviewer2")
        self.assertEqual(corpus_report.corpus, self.corpus)
#pylint: enable=E1101
