'''vector_db tests'''
import os
import faiss
import numpy as np
from contextlib import contextmanager
from django.test import TestCase
from django.conf import settings
from ui.models import Keyword, Chunk, Document, Corpus
from vector_db.faiss_db import FAISSIndex, encode_chunk, VectorDB

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
        self.dimension = 768
        self.faiss_index = FAISSIndex(dimension=self.dimension)
        self.test_vectors = np.random.rand(100, self.dimension).astype('float32')

    def tearDown(self):
        self.omp_manager.__exit__(None, None, None)

    def test_initialization(self):
        self.assertEqual(self.faiss_index.dimension, self.dimension)
        self.assertEqual(self.faiss_index.ntotal, 0)

    def test_add_vectors(self):
        progress_values = []
        def progress_callback(p):
            progress_values.append(p)

        self.faiss_index.add_vectors(
            self.test_vectors,
            batch_size=10,
            progress_callback=progress_callback
        )

        self.assertEqual(self.faiss_index.ntotal, 100)
        self.assertTrue(len(progress_values) > 1)
        self.assertAlmostEqual(progress_values[-1], 1.0)

    def test_search_vectors(self):
        self.faiss_index.add_vectors(self.test_vectors)
        query = self.test_vectors[0]

        distances, indices = self.faiss_index.search_vectors(query, k=5)

        self.assertEqual(distances.shape, (1, 5))
        self.assertEqual(indices.shape, (1, 5))
        self.assertEqual(indices[0][0], 0)

    def test_invalid_dimension(self):
        with self.assertRaises(ValueError):
            FAISSIndex(dimension=0)

    def test_invalid_vectors(self):
        invalid_vectors = np.random.rand(10, self.dimension + 1)
        with self.assertRaises(ValueError):
            self.faiss_index.add_vectors(invalid_vectors)

    def test_empty_vectors(self):
        empty_vectors = np.array([], dtype=np.float32).reshape(0, self.dimension)
        self.faiss_index.add_vectors(empty_vectors)
        self.assertEqual(self.faiss_index.ntotal, 0)


class TestVectorDB(TestCase):
    def setUp(self):
        self.omp_manager = OpenMPManager()
        self.omp_manager.__enter__()
        self.dimension = 768
        self.test_index_path = "test_faiss_index.bin"
        # Initialize vector DB with in-memory FAISS index
        self.db = VectorDB(dimension=self.dimension)
        self.db.index_path = self.test_index_path
        self.test_vectors = np.random.rand(5, self.dimension).astype('float32')
        self.test_metadata = [
            {"id": i, "text": f"Test vector {i}"}
            for i in range(len(self.test_vectors))
        ]
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
        self.chunk1 = Chunk.objects.create(
            document=self.document,
            seq=1,
            chunk_txt="This is a test chunk1.",
            vector=encode_chunk("This is a test chunk1.").tolist(),
            chunk_size=100
        )


    def tearDown(self):
        # Clean up any temporary files
        if os.path.exists(self.test_index_path):
            os.remove(self.test_index_path)
        # Clear the vector database
        self.db = None
        self.omp_manager.__exit__(None, None, None)

    def test_init(self):
        """Test VectorDB initialization"""
        self.assertEqual(self.db.dimension, self.dimension)
        self.assertIsNotNone(self.db.faiss_index)

    def test_store_and_load_index(self):

        # Add test vectors to the index
        self.db.store_chunk_vectors([self.chunk, self.chunk1])
        # Save index
        self.db.save_index()
        # Create new DB instance and load saved index
        newdb = VectorDB(dimension=self.dimension)
        newdb.index_path =  self.test_index_path
        newdb.load_index()
        # Verify loaded index works
        query = np.random.rand(self.dimension).astype('float32')
        original_results = self.db.faiss_index.search_vectors(query, k=1)
        loaded_results = newdb.faiss_index.search_vectors(query, k=1)
        self.assertEqual(original_results, loaded_results)

    def test_search_similar_chunks(self):
        """Test similarity search"""
        # Store some test vectors
        chunks = [
            self.chunk,
            self.chunk1
        ]
        self.db.store_chunk_vectors([self.chunk, self.chunk1])

        # Search
        query = "test query"
        distances, indices = self.db.search_similar_chunks(query)

        self.assertIsInstance(distances, np.ndarray)
        self.assertIsInstance(indices, np.ndarray)
        self.assertTrue(len(distances) > 0)
        self.assertTrue(len(indices) > 0)

class TestChunkStorage(TestCase):
    def setUp(self):
        self.db = VectorDB()
        self.test_chunks = [
            Chunk.objects.create(chunk_txt=f"Test chunk {i}")
            for i in range(5)
        ]

    def test_store_and_retrieve(self):
        self.db.store_chunks(self.test_chunks)
        results = self.db.search_similar("Test chunk 0")
        self.assertEqual(len(results), 5)
        self.assertEqual(results[0].chunk_txt, "Test chunk 0")

class TestVectorDB2(TestCase):
    def setUp(self):
        self.dimension = 768
        self.test_index_path = "test_faiss.index"
        self.db = VectorDB(dimension=self.dimension)
        self.test_vectors = np.random.rand(100, self.dimension).astype('float32')
        self.test_chunk_ids = list(range(100))

    def tearDown(self):
        if os.path.exists(self.test_index_path):
            os.remove(self.test_index_path)
        if os.path.exists(f"{self.test_index_path}.chunk_ids.npy"):
            os.remove(f"{self.test_index_path}.chunk_ids.npy")

    def test_init(self):
        self.assertEqual(self.db.dimension, self.dimension)
        self.assertEqual(self.db.faiss_index.ntotal, 0)

    def test_add_vectors_batch(self):
        progress_calls = []
        def progress_cb(p):
            progress_calls.append(p)

        self.db.add_vectors(
            self.test_vectors,
            chunk_ids=self.test_chunk_ids,
            batch_size=10,
            progress_callback=progress_cb
        )

        self.assertEqual(self.db.faiss_index.ntotal, 100)
        self.assertEqual(len(progress_calls), 10)
        self.assertAlmostEqual(progress_calls[-1], 1.0)

    def test_search_vectors(self):
        self.db.add_vectors(self.test_vectors, self.test_chunk_ids)
        query = self.test_vectors[0]

        results = self.db.search(query, k=5)

        self.assertEqual(len(results), 5)
        self.assertEqual(results[0][1], self.test_chunk_ids[0])
        self.assertAlmostEqual(results[0][0], 0.0, places=5)

    def test_save_load_index(self):
        self.db.add_vectors(self.test_vectors, self.test_chunk_ids)
        self.db.save_index(self.test_index_path)

        new_db = VectorDB(dimension=self.dimension)
        new_db.load_index(self.test_index_path)

        self.assertEqual(new_db.faiss_index.ntotal, 100)
        self.assertEqual(len(new_db.chunk_ids), 100)

    def test_invalid_vectors(self):
        wrong_dim = np.random.rand(10, self.dimension + 1)
        with self.assertRaises(ValueError):
            self.db.add_vectors(wrong_dim, list(range(10)))

    def test_mismatched_chunk_ids(self):
        with self.assertRaises(ValueError):
            self.db.add_vectors(self.test_vectors, chunk_ids=list(range(50)))

