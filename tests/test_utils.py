import unittest
import sys
import os

# Add src directory to path
sys.path.append(os.path.abspath("src"))
import utils

class TestUtils(unittest.TestCase):
    
    def test_is_english(self):
        # Clear English
        self.assertTrue(utils.is_english("This is a clear English sentence."))
        self.assertTrue(utils.is_english("Peace in the Middle East."))
        
        # Clear Non-English
        self.assertFalse(utils.is_english("هذا نص عربي")) # Arabic
        self.assertFalse(utils.is_english("Это русский текст")) # Russian
        self.assertFalse(utils.is_english("这是一个中文句子")) # Chinese
        self.assertFalse(utils.is_english("Ez egy magyar mondat")) # Hungarian (high ASCII but non-English words)
        
        # Helper might fail short sentences without common words, but let's test expected behavior
        self.assertTrue(utils.is_english("What happened?")) # Short but high ASCII

    def test_normalize_keyword(self):
        # Mappings
        self.assertEqual(utils.normalize_keyword("Palestinians"), "palestine")
        self.assertEqual(utils.normalize_keyword("Gazans"), "gaza")
        
        # Stemming
        self.assertEqual(utils.normalize_keyword("bombing"), "bomb")
        self.assertEqual(utils.normalize_keyword("wars"), "war")
        self.assertEqual(utils.normalize_keyword("countries"), "country")
        
        # Cleaning
        self.assertEqual(utils.normalize_keyword("Israel!"), "israel")
        self.assertEqual(utils.normalize_keyword("peace..."), "peace")

    def test_parse_duration(self):
        self.assertEqual(utils.parse_duration("PT1M"), 60)
        self.assertEqual(utils.parse_duration("PT1H"), 3600)
        self.assertEqual(utils.parse_duration("PT1M30S"), 90)
        self.assertEqual(utils.parse_duration("PT30S"), 30)

if __name__ == '__main__':
    unittest.main()
