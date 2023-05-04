import unittest
from unittest.mock import patch
import requests

from backend import app
import scrapper


class TestApp(unittest.TestCase):

    @patch('requests.get')
    def test_search_route(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "results": [
                {
                    "title": "Test Recipe 1",
                    "href": "http://testrecipe1.com",
                    "rating": 4.5,
                    "reviews": 10
                },
                {
                    "title": "Test Recipe 2",
                    "href": "http://testrecipe2.com",
                    "rating": 3.8,
                    "reviews": 5
                }
            ]
        }
        with app.test_client() as client:
            response = client.get('/search?query=test')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Recipe 1', response.data)
            self.assertIn(b'Test Recipe 2', response.data)

    def test_scrape_recipes(self):
        recipes = scrapper()
        self.assertGreater(len(recipes), 0)
        for recipe in recipes:
            self.assertIsNotNone(recipe['title'])
            self.assertIsNotNone(recipe['href'])
            self.assertIsNotNone(recipe['rating'])
            self.assertIsNotNone(recipe['reviews'])
            self.assertIsInstance(recipe['title'], str)
            self.assertIsInstance(recipe['href'], str)
            self.assertIsInstance(recipe['rating'], float)
            self.assertIsInstance(recipe['reviews'], int)


if __name__ == '__main__':
    unittest.main()
