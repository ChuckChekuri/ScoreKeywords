'''vector_db tests'''
import os
import faiss
import numpy as np
from contextlib import contextmanager
from django.test import TestCase
from ui.models import Chunk, Document, Corpus
from vector_db.faiss_db import FAISSIndex, encode_chunk

class OpenMPManager:
    def __init__(self):
        self.original_setting = None
    
    def __enter__(self):
        self.original_setting = os.environ.get('KMP_DUPLICATE_LIB_OK')
        os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.original_setting is not None:
            os.environ['KMP_DUPLICATE_LIB_OK'] = self.original_setting
        else:
            del os.environ['KMP_DUPLICATE_LIB_OK']

class FAISSIndexTests(TestCase):
    '''Tests for FAISSIndex'''
    
    def setUp(self):
        self.omp_manager = OpenMPManager()
        self.omp_manager.__enter__()
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
            num_chunks=5
        )
        self.chunk = Chunk.objects.create(
            document=self.document,
            seq=1,
            chunk_txt="This is a test chunk.",
            vector=encode_chunk("This is a test chunk.").tolist(),
            chunk_size=100
        )
    
    def tearDown(self):
        self.omp_manager.__exit__(None, None, None)
    
    def test_encode_chunk(self):
        '''Test encoding a chunk'''
        chunk_text = "This is a test chunk."
        vector = encode_chunk(chunk_text)
        self.assertEqual(np.array(vector).shape, (1, 128))


    def test_add_vectors(self):
        '''Test adding vectors to the FAISS index'''
        faiss_index = FAISSIndex(dimension=128)
        vectors = encode_chunk(chunk_text="This is a test chunk.").tolist()
        vectors = np.vstack(vectors)
        faiss_index.add_vectors(vectors)
        self.assertEqual(faiss_index.index.ntotal, 1)

    def test_search_vectors(self):
        '''Test searching for similar vectors'''
        with OpenMPManager():
            faiss_index = FAISSIndex(dimension=128)
            chunk_text = "This is a test chunk."
            vector = encode_chunk(chunk_text=chunk_text)

            # Add vector to FAISS index
            vectors = np.array(vector)
            faiss_index.add_vectors(vectors)

            # Search for the vector
            query_vector = np.array(vector)
            distances, indices = faiss_index.search_vectors(query_vector, k=1)
            
            # Add assertions
            self.assertEqual(len(distances), 1)
            self.assertEqual(len(indices), 1)
            self.assertAlmostEqual(distances[0][0], 0.0, places=5)
