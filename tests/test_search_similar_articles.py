import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from src.backend.main import search_similar_articles

class TestSearchSimilarArticles(unittest.TestCase):

    @patch("src.backend.main.index")
    @patch("src.backend.main.metadata")
    def test_search_similar_articles(self, mock_metadata, mock_index):
        """Test that search_similar_articles returns the correct search results."""
        
        # Mock FAISS index response: distances and indices
        mock_index.search.return_value = (
            np.array([[0.1, 0.2, 0.3]]),  # Distances
            np.array([[0, 1, 2]])         # Indices of mock results
        )
        
        # Mock metadata for the articles
        mock_metadata.__getitem__.side_effect = [
            {"title": "Article 1", "summary": "Summary 1", "content": "Content 1", "url": "http://example.com/1"},
            {"title": "Article 2", "summary": "Summary 2", "content": "Content 2", "url": "http://example.com/2"},
            {"title": "Article 3", "summary": "Summary 3", "content": "Content 3", "url": "http://example.com/3"},
        ]
        
        # Create a mock embedding for the query
        query_embedding = np.array([0.5, 0.5, 0.5, 0.5])

        # Call the function under test
        results = search_similar_articles(query_embedding, top_k=3)

        # Verify the number of results returned
        self.assertEqual(len(results), 3)

        # Verify the content of each result
        expected_results = [
            {"title": "Article 1", "summary": "Summary 1", "content": "Content 1", "url": "http://example.com/1", "score": 0.1},
            {"title": "Article 2", "summary": "Summary 2", "content": "Content 2", "url": "http://example.com/2", "score": 0.2},
            {"title": "Article 3", "summary": "Summary 3", "content": "Content 3", "url": "http://example.com/3", "score": 0.3},
        ]
        
        for i, result in enumerate(results):
            self.assertEqual(result["title"], expected_results[i]["title"])
            self.assertEqual(result["summary"], expected_results[i]["summary"])
            self.assertEqual(result["content"], expected_results[i]["content"])
            self.assertEqual(result["url"], expected_results[i]["url"])
            self.assertAlmostEqual(result["score"], expected_results[i]["score"], places=2)

if __name__ == "__main__":
    unittest.main()
