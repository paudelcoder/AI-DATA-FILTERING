import unittest
import os
import sys
# Add the parent directory to the path to import the web_interface module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from web_interface.app import app

class WebInterfaceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_graph_data_endpoint(self):
        response = self.app.get('/graph_data')
        self.assertEqual(response.status_code, 200)
        self.assertIn('nodes', response.json)
        self.assertIn('links', response.json)

if __name__ == '__main__':
    unittest.main()
