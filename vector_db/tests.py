'''vector_db tests'''
import faiss
import numpy as np
from django.test import TestCase
from ui.models import Chunk, Document, Corpus
from vector_db.faiss_db import FAISSIndex, encode_chunk

class FAISSIndexTests(TestCase):
    '''Tests for FAISSIndex'''
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
            num_chunks=5
        )
        self.chunk = Chunk.objects.create(
            document=self.document,
            seq=1,
            chunk_txt="This is a test chunk.",
            vector=encode_chunk("This is a test chunk.").tolist(),
            chunk_size=100
        )

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
        faiss_index = FAISSIndex(dimension=128)
        chunk_text = "This is a test chunk."
        vector = encode_chunk(chunk_text=chunk_text)

        # Add vector to FAISS index
        vectors = np.array(vector)
        faiss_index.add_vectors(vectors)

        # Search for the vector
        query_vector = np.array(vector)
        distances, indices = faiss_index.search_vectors(query_vector, k=1)
        self.assertEqual(len(indices), 1)
        self.assertEqual(indices[0][0], 0)
