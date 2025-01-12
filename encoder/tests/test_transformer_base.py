import os
import shutil
import torch
import numpy as np
from django.test import TestCase
from django.conf import settings
from ..services.transformer_base import TransformerEncoderBase

class TestTransformerBase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model_name = 'bert-base-uncased'
        cls.encoder = TransformerEncoderBase(cls.model_name)
        cls.dimension = settings.TRANSFORMER_SETTINGS['models'][cls.model_name]['dimension']
        cls.batch_size = settings.TRANSFORMER_SETTINGS['models'][cls.model_name]['batch_size']

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_initialization(self):
        self.assertIsNotNone(self.encoder.model)
        self.assertIsNotNone(self.encoder.tokenizer)
        self.assertEqual(self.encoder.dimension, self.dimension)
        self.assertEqual(self.encoder.batch_size, self.batch_size)
        self.assertTrue(os.path.exists(self.encoder.cache_dir))
        self.assertIsNotNone(self.encoder.model.pooler.dense.weight.data.sum())
        self.assertEqual(self.encoder.model.pooler.dense.bias.data.sum(), 0)

    def test_device_handling(self):
        expected_device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.assertEqual(str(self.encoder.device), expected_device)
        self.assertEqual(str(self.encoder.model.device), expected_device)

    def test_encode_text(self):
        text = "This is a test sentence."
        embedding = self.encoder.encode_text(text)
        self.assertIsInstance(embedding, np.ndarray)
        self.assertEqual(len(embedding), self.dimension)

    def test_encode_batch(self):
        texts = ["First test.", "Second test."]
        embeddings = self.encoder.encode_batch(texts)
        self.assertIsInstance(embeddings, np.ndarray)
        self.assertEqual(embeddings.shape, (len(texts), self.dimension))

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            self.encoder.encode_text("")
        with self.assertRaises(ValueError):
            self.encoder.encode_text(" ")
        with self.assertRaises(ValueError):
            self.encoder.encode_batch([])

    def test_encoding_consistency(self):
        text = "Test sentence."
        embedding1 = self.encoder.encode_text(text)
        embedding2 = self.encoder.encode_text(text)
        np.testing.assert_array_almost_equal(embedding1, embedding2)


    def test_dimension_property(self):
        self.assertEqual(self.encoder.dimension(), self.dimension)
        self.assertIsInstance(self.encoder.dimension(), int)

    def test_long_text_handling(self):
        long_text = " ".join(["word"] * 1000)
        embedding = self.encoder.encode_text(long_text)
        self.assertEqual(len(embedding), self.dimension)

    def test_batch_size_handling(self):
        large_batch = ["Test sentence."] * 10
        embeddings = self.encoder.encode_batch(large_batch)
        self.assertEqual(embeddings.shape, (len(large_batch), self.dimension))
