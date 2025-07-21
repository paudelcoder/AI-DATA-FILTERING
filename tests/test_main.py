import unittest
from unittest.mock import patch, MagicMock
from hinduism_ai.main import HinduismAI, DatabaseManager

class TestHinduismAI(unittest.TestCase):

    def setUp(self):
        self.ai = HinduismAI()
        self.db_manager = DatabaseManager(db_name=":memory:")

    def test_extract_verses(self):
        text = "1. This is a verse.\n2. This is another verse."
        doc = self.ai.load_text(text)
        verses = self.ai.extract_verses(doc)
        self.assertEqual(len(verses), 2)
        self.assertEqual(verses[0], "1. This is a verse.")

    def test_extract_concepts(self):
        text = "This sentence talks about Brahman. This one talks about Atman."
        doc = self.ai.load_text(text)
        concepts = self.ai.extract_concepts(doc, ["Brahman", "Atman"])
        self.assertEqual(len(concepts), 2)

    @patch('hinduism_ai.main.requests.get')
    def test_main_cli_scrape(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html><body><h1>Test Title</h1><p>1. A verse.\n</p><p>A concept about Brahman.</p></body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with patch('builtins.input', side_effect=['1', 'http://test.com', 'Test Title', 'Brahman', '5']):
            with patch('hinduism_ai.main.DatabaseManager') as mock_db_manager:
                instance = mock_db_manager.return_value
                instance.add_source.return_value = 1
                from hinduism_ai.main import main_cli
                main_cli()
                instance.add_verses.assert_called_once()
                instance.add_concepts.assert_called_once()

if __name__ == '__main__':
    unittest.main()
