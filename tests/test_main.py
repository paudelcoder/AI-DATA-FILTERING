import unittest
from hinduism_ai.main import HinduismAI
import spacy

class TestHinduismAI(unittest.TestCase):

    def setUp(self):
        self.ai = HinduismAI()
        self.nlp = spacy.load("en_core_web_sm")
        self.sample_text = """
        The Upanishads are a collection of texts that contain some of the central philosophical concepts of Hinduism.
        They are considered by Hindus to contain revealed truths (Sruti) concerning the nature of ultimate reality (brahman) and describing the character and form of human salvation (moksha).
        The Bhagavad Gita is a 700-verse Hindu scripture that is part of the Hindu epic Mahabharata.
        """
        self.doc = self.nlp(self.sample_text)

    def test_filter_content(self):
        filtered = self.ai.filter_content(self.doc, ["Upanishads", "Gita"])
        self.assertEqual(len(filtered), 2)
        self.assertIn("Upanishads", filtered[0])
        self.assertIn("Gita", filtered[1])

    def test_save_and_get_data(self):
        filtered = self.ai.filter_content(self.doc, ["Hinduism"])
        self.ai.save_data(filtered)
        saved_data = self.ai.get_saved_data()
        self.assertEqual(len(saved_data), 1)
        self.assertIn("Hinduism", saved_data[0])

    def test_get_common_words(self):
        filtered = self.ai.filter_content(self.doc, ["the"])
        self.ai.save_data(filtered)
        common_words = self.ai.get_common_words(5)
        # Expected result may vary based on tokenization, but 'the' should be prominent
        self.assertIn('the', [word[0].lower() for word in common_words])

if __name__ == '__main__':
    unittest.main()
