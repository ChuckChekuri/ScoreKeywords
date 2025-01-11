import os
from django.test import TestCase
from django.apps import apps

class EncoderAppStructureTest(TestCase):
    def test_app_directories_exist(self):
        app_path = apps.get_app_config('encoder').path
        
        # Test required directories exist
        self.assertTrue(os.path.exists(os.path.join(app_path, 'services')))
        self.assertTrue(os.path.exists(os.path.join(app_path, 'interfaces')))
        self.assertTrue(os.path.exists(os.path.join(app_path, 'tests')))

    def test_app_is_installed(self):
        self.assertTrue(apps.is_installed('encoder'))
