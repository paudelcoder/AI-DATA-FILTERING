import unittest
import os
from hinduism_ai.main import HinduismAI, DatabaseManager
import spacy

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.db_name = "test_hinduism_data.db"
        self.ai = HinduismAI()
        self.db_manager = DatabaseManager(db_name=self.db_name)
        self.nlp = spacy.load("en_core_web_sm")
        self.sample_text = """
1. The Upanishads are a collection of texts.
2. They discuss concepts like Brahman and Atman.
The Bhagavad Gita is another key text.
        """
        self.doc = self.nlp(self.sample_text)

    def tearDown(self):
        os.remove(self.db_name)

    def test_full_pipeline(self):
        # 1. Add a source
        source_id = self.db_manager.add_source("http://example.com", "Test Text")
        self.assertIsNotNone(source_id)

        # 2. Extract and store verses
        verses = self.ai.extract_verses(self.doc)
        self.db_manager.add_verses(source_id, verses)
        stored_verses = self.db_manager.conn.execute("SELECT * FROM verses WHERE source_id = ?", (source_id,)).fetchall()
        self.assertEqual(len(stored_verses), 2)

        # 3. Extract and store concepts
        concepts = self.ai.extract_concepts(self.doc, ["Brahman", "Atman"])
        self.db_manager.add_concepts(source_id, concepts)
        stored_concepts = self.db_manager.conn.execute("SELECT * FROM concepts WHERE source_id = ?", (source_id,)).fetchall()
        self.assertEqual(len(stored_concepts), 1)

if __name__ == '__main__':
    unittest.main()
