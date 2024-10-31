import unittest
import numpy as np
from src.data_import.store_embeddings_faiss import parse_embedding

class TestParseEmbedding(unittest.TestCase):

    def test_parse_valid_embedding(self):
        """Test that parse_embedding correctly parses a valid embedding string."""
        embedding_str = "[1.0, 2.0, 3.0, 4.0]"
        result = parse_embedding(embedding_str)
        
        # Check that the result is a numpy array of type float32
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.dtype, np.float32)
        
        # Check that the values in the array are correct
        np.testing.assert_array_equal(result, np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float32))

    def test_parse_float64_embedding(self):
        """Test that parse_embedding converts a float64 embedding to float32."""
        embedding_str = "[1.0, 2.0, 3.0, 4.0]"
        result = parse_embedding(embedding_str)

        # Check that the dtype is float32
        self.assertEqual(result.dtype, np.float32)
        # Verify values are correct and the type has been cast to float32
        self.assertTrue(all(isinstance(x, np.float32) for x in result))

if __name__ == "__main__":
    unittest.main()
