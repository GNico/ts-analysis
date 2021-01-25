from django.test import TestCase

from .models import Client


class ClientModelTest(TestCase):

    def test_string_representation(self):
        client = Client(name="Some client")
        self.assertEqual(str(client), client.name)