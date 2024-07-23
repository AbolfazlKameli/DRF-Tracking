from django.test import TestCase
from model_bakery import baker

from home.models import Writer


class TestWriteModel(TestCase):
    def setUp(self):
        self.writer = baker.make(Writer, first_name='kevin', last_name='brown')

    def test_writer_str(self):
        self.assertEqual(str(self.writer), 'kevin brown')
