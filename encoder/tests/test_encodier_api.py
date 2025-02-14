import numpy as np
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from encoder.services.transformer_base import BertEncoder, AlbertEncoder, RobertaEncoder

class EncodingAPIViewTests(APITestCase):

    def setUp(self):
        # Assumes your urls.py maps the view with name 'api-encode'
        self.url = reverse('api-encode')

    def test_missing_text(self):
        data = {}  # No "text" provided
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_unsupported_model(self):
        data = {"text": "Hello, world!", "model": "unsupported"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertIn("Unsupported model", response.data["error"])

    def _patch_encode_method(self, encoder_cls, return_value):
        """
        Patch the encode method on the encoder class to return a fixed value.
        Returns the original method so it can be restored after test.
        """
        original_encode = encoder_cls.encode

        def fake_encode(self, text):
            return return_value

        encoder_cls.encode = fake_encode
        return original_encode

    def _restore_encode_method(self, encoder_cls, original_encode):
        encoder_cls.encode = original_encode

    def test_bert_encoder_success(self):
        expected_output = np.array([0.1, 0.2, 0.3])
        original_encode = self._patch_encode_method(BertEncoder, expected_output)
        data = {"text": "Test text", "model": "bert"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("encoded", response.data)
        # Compare each element from response with expected output
        self.assertTrue(np.allclose(np.array(response.data["encoded"]), expected_output))
        self._restore_encode_method(BertEncoder, original_encode)

    def test_albert_encoder_success(self):
        expected_output = np.array([0.4, 0.5, 0.6])
        original_encode = self._patch_encode_method(AlbertEncoder, expected_output)
        data = {"text": "Test text", "model": "albert"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("encoded", response.data)
        self.assertTrue(np.allclose(np.array(response.data["encoded"]), expected_output))
        self._restore_encode_method(AlbertEncoder, original_encode)

    def test_roberta_encoder_success(self):
        expected_output = np.array([0.7, 0.8, 0.9])
        original_encode = self._patch_encode_method(RobertaEncoder, expected_output)
        data = {"text": "Test text", "model": "roberta"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("encoded", response.data)
        self.assertTrue(np.allclose(np.array(response.data["encoded"]), expected_output))
        self._restore_encode_method(RobertaEncoder, original_encode)

    def test_encoding_exception(self):
        # Patch BertEncoder to raise an exception when encode is called.
        original_encode = BertEncoder.encode

        def fake_encode_error(self, text):
            raise Exception("Encoding error")

        BertEncoder.encode = fake_encode_error
        data = {"text": "Test text", "model": "bert"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Encoding error")
        # Restore original encode method
        BertEncoder.encode = original_encode
