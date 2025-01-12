import os
import shutil
import torch
import numpy as np
from django.test import TestCase
from django.conf import settings
from ..services.transformer_base import TransformerEncoderBase, BertEncoder, AlbertEncoder, RobertaEncoder
class TransformerEncodersTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.encoders = [
            ('bert-base-uncased', BertEncoder()),
            ('albert-base-v2', AlbertEncoder()),
            ('roberta-base', RobertaEncoder())
        ]
        cls.test_text = "This is a test sentence."
        cls.test_texts = ["First test sentence.", "Second test sentence."]

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    
    def test_model_initialization(self):
        for name, encoder in self.encoders:
            print(f'Name: {name}')
            print(f'Encoder : {encoder}')
            with self.subTest(encoder=encoder):
                self.assertIsNotNone(encoder)
                self.assertIsNotNone(encoder.tokenizer)
                self.assertTrue(os.path.exists(self.encoder.cache_dir))

    def test_encode_single_text(self):
        for name, encoder in self.encoders:
            with self.subTest(encoder=name):
                vector = encoder.encode_text(self.test_text)
                self.assertIsInstance(vector, np.ndarray)
                self.assertEqual(len(vector), encoder.dimension())

    def test_encode_batch_texts(self):
        for name, encoder in self.encoders:
            with self.subTest(encoder=name):
                vectors = encoder.encode_batch(self.test_texts)
                self.assertIsInstance(vectors, np.ndarray)
                self.assertEqual(vectors.shape, (len(self.test_texts), encoder.dimension()))

    def test_device_handling(self):
        for name, encoder in self.encoders:
            with self.subTest(encoder=name):
                expected_device = 'cuda' if torch.cuda.is_available() else 'cpu'
                self.assertEqual(str(encoder.device), expected_device)
                self.assertEqual(str(encoder.model.device), expected_device)

    def test_model_caching(self):
        for name, encoder in self.encoders:
            with self.subTest(encoder=name):
                # Test if model files exist in cache
                self.assertTrue(os.path.exists(self.cache_dir))
                cached_files = os.listdir(self.cache_dir)
                self.assertGreater(len(cached_files), 0)

    def test_encoding_consistency(self):
        for name, encoder in self.encoders:
            with self.subTest(encoder=name):
                # Test if multiple encodings of same text are consistent
                vector1 = encoder.encode_text(self.test_text)
                vector2 = encoder.encode_text(self.test_text)
                np.testing.assert_array_almost_equal(vector1, vector2)

    def test_empty_input_handling(self):
        for name, encoder in self.encoders:
            with self.subTest(encoder=name):
                with self.assertRaises(ValueError):
                    encoder.encode_text("")
                with self.assertRaises(ValueError):
                    encoder.encode_batch([])

    def test_long_text_truncation(self):
        long_text = " ".join(["test"] * 1000)
        for name, encoder in self.encoders:
            with self.subTest(encoder=name):
                vector = encoder.encode_text(long_text)
                self.assertEqual(len(vector), encoder.dimension())

    def test_batch_size_limits(self):
        large_batch = ["Test sentence."] * 100
        for name, encoder in self.encoders:
            with self.subTest(encoder=name):
                vectors = encoder.encode_batch(large_batch)
                self.assertEqual(vectors.shape, (len(large_batch), encoder.dimension()))

    def test_dimension_consistency(self):
        for name, encoder in self.encoders:
            with self.subTest(encoder=name):
                self.assertEqual(encoder.dimension(), settings.TRANSFORMER_SETTINGS['models'][name]['dimension'])
