import requests
from typing import List, Literal, Optional
from enum import Enum

from pydantic import BaseModel, Field

HN_URL = "https://hacker-news.firebaseio.com/v0/"


class ItemType(Enum):
    """
    Enum class to represent the type of story
    """

    JOB = "job"
    STORY = "story"
    COMMENT = "comment"
    POLL = "poll"
    POLLOPT = "pollopt"


class Item(BaseModel):
    """
    Story class to represent a story from Hacker News
    """

    id: int = Field(alias="id", examples=[1, 2, 3])
    deleted: Optional[bool] = Field(
        alias="deleted", examples=[True, False], default=False
    )
    type: ItemType = Field(
        alias="type",
        examples=[
            ItemType.JOB,
            ItemType.STORY,
            ItemType.COMMENT,
            ItemType.POLL,
            ItemType.POLLOPT,
        ],
    )
    by: str = Field(alias="by", examples=["author1", "author2", "author3"])
    time: int = Field(alias="time", examples=[1615767531, 1615767532, 1615767533])
    text: Optional[str] = Field(
        alias="text", examples=["text1", "text2", "text3"], default=None
    )
    dead: Optional[bool] = Field(alias="dead", examples=[True, False], default=False)
    parent: Optional[int] = Field(alias="parent", examples=[1, 2, 3], default=None)
    poll: Optional[int] = Field(alias="poll", examples=[1, 2, 3], default=None)
    kids: List[int] = Field(alias="kids", examples=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    url: str = Field(alias="url", examples=["url1", "url2", "url3"])
    score: int = Field(alias="score", examples=[1, 2, 3])
    title: str = Field(alias="title", examples=["title1", "title2", "title3"])
    parts: Optional[List[int]] = Field(
        alias="parts", examples=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], default=None
    )
    descendants: int = Field(alias="descendants", examples=[1, 2, 3])

    def __str__(self):
        return f"{self.title} by {self.by} ({self.url})"

    def is_story(self) -> bool:
        """
        Check if the item is a story
        """
        return self.type == ItemType.STORY


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

    def get_item(self, item_id: int) -> Item:
        """
        Get a story from Hacker News
        """
        url = f"{HN_URL}item/{item_id}.json"
        response = self.session.get(url)
        response.raise_for_status()
        story = response.json()
        return Item(**story)


if __name__ == "__main__":

    hn = HackerNews()
    top_stories = hn.get_top_stories()
    print(top_stories)
    best_stories = hn.get_best_stories()
    print(best_stories)
    new_stories = hn.get_new_stories()
    print(new_stories)
    story = hn.get_item(top_stories[0])
    print(story)
