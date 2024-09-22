import requests
from typing import List

HN_URL = "https://hacker-news.firebaseio.com/v0/"


class HackerNews:
    """
    HackerNews class to interact with the Hacker News API
    """

    def __init__(self):
        self.session = requests.Session()

    def get_top_stories(self, limit: int = 10) -> List[int]:
        """
        Get the top stories from Hacker News
        """
        url = f'{HN_URL}topstories.json?orderBy="$key"&limitToFirst={limit}'
        response = self.session.get(url)
        response.raise_for_status()
        top_stories = response.json()
        return top_stories

    def get_best_stories(self, limit: int = 10) -> List[int]:
        """
        Get the best stories from Hacker News
        """
        url = f'{HN_URL}beststories.json?orderBy="$key"&limitToFirst={limit}'
        response = self.session.get(url)
        response.raise_for_status()
        best_stories = response.json()
        return best_stories

    def get_new_stories(self, limit: int = 10) -> List[int]:
        """
        Get the new stories from Hacker News
        """
        url = f'{HN_URL}newstories.json?orderBy="$key"&limitToFirst={limit}'
        response = self.session.get(url)
        response.raise_for_status()
        new_stories = response.json()
        return new_stories
