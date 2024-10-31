import unittest
import numpy as np
from src.data_import.generate_embeddings import create_embedding

class TestCreateEmbedding(unittest.TestCase):

    def test_create_embedding_with_text(self):
        """Test that create_embedding returns a valid embedding for a non-empty string."""
        text = "This is a test sentence."
        embedding = create_embedding(text)

        # Check that the result is a list
        self.assertIsInstance(embedding, list, "Embedding should be a list.")
        
        # Check that the list contains floats and is not empty
        self.assertTrue(all(isinstance(x, float) for x in embedding), "All elements in the embedding should be floats.")
        self.assertGreater(len(embedding), 0, "Embedding should not be empty.")

    def test_create_embedding_with_empty_text(self):
        """Test that create_embedding returns np.nan for an empty or None text."""
        empty_text = None
        embedding = create_embedding(empty_text)
        
        # Check that the result is np.nan
        self.assertTrue(np.isnan(embedding), "Embedding should be NaN for empty or None text.")

    def test_create_embedding_with_different_texts(self):
        """Test that embeddings are different for different input texts."""
        text1 = "This is the first sentence."
        text2 = "This is a different sentence."
        
        embedding1 = create_embedding(text1)
        embedding2 = create_embedding(text2)
        
        # Check that embeddings for different texts are not the same
        self.assertNotEqual(embedding1, embedding2, "Embeddings should differ for different input texts.")

if __name__ == "__main__":
    unittest.main()
