import unittest
from unittest.mock import patch
from bitesize.hn_interface import HackerNews


class TestHackerNews(unittest.TestCase):

    @patch("requests.Session.get")
    def test_get_top_stories(self, mock_get):
        mock_get.return_value.json.return_value = [1, 2, 3, 4, 5]
        mock_get.return_value.raise_for_status = lambda: None

        hn = HackerNews()
        top_stories = hn.get_top_stories(5)
        self.assertEqual(top_stories, [1, 2, 3, 4, 5])
        mock_get.assert_called_once_with(
            'https://hacker-news.firebaseio.com/v0/topstories.json?orderBy="$key"&limitToFirst=5'
        )

    @patch("requests.Session.get")
    def test_get_best_stories(self, mock_get):
        mock_get.return_value.json.return_value = [6, 7, 8, 9, 10]
        mock_get.return_value.raise_for_status = lambda: None

        hn = HackerNews()
        best_stories = hn.get_best_stories(5)
        self.assertEqual(best_stories, [6, 7, 8, 9, 10])
        mock_get.assert_called_once_with(
            'https://hacker-news.firebaseio.com/v0/beststories.json?orderBy="$key"&limitToFirst=5'
        )

    @patch("requests.Session.get")
    def test_get_new_stories(self, mock_get):
        mock_get.return_value.json.return_value = [11, 12, 13, 14, 15]
        mock_get.return_value.raise_for_status = lambda: None

        hn = HackerNews()
        new_stories = hn.get_new_stories(5)
        self.assertEqual(new_stories, [11, 12, 13, 14, 15])
        mock_get.assert_called_once_with(
            'https://hacker-news.firebaseio.com/v0/newstories.json?orderBy="$key"&limitToFirst=5'
        )


if __name__ == "__main__":
    unittest.main()
