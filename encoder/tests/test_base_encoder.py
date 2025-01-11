from django.test import TestCase
import numpy as np
from ..interfaces.base_encoder import BaseEncoder

class MockEncoder(BaseEncoder):
    def encode_text(self, text: str) -> np.ndarray:
        return np.zeros(5)

    def encode_batch(self, texts: list[str]) -> np.ndarray:
        return np.zeros((len(texts), 5))

    def dimension(self) -> int:
        return 5

class BaseEncoderTest(TestCase):
    def setUp(self):
        self.encoder = MockEncoder()

    def test_encode_text_returns_vector(self):
        vector = self.encoder.encode_text("test")
        self.assertIsInstance(vector, np.ndarray)
        self.assertEqual(vector.shape, (5,))

    def test_encode_batch_returns_matrix(self):
        matrix = self.encoder.encode_batch(["test1", "test2"])
        self.assertIsInstance(matrix, np.ndarray)
        self.assertEqual(matrix.shape, (2, 5))

    def test_dimension_returns_int(self):
        dim = self.encoder.dimension()
        self.assertIsInstance(dim, int)
        self.assertEqual(dim, 5)
