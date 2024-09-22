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
    kids: Optional[List[int]] = Field(
        alias="kids", examples=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], default=None
    )
    url: Optional[str] = Field(
        alias="url", examples=["url1", "url2", "url3"], default=None
    )
    score: Optional[int] = Field(alias="score", examples=[1, 2, 3], default=None)
    title: Optional[str] = Field(
        alias="title", examples=["title1", "title2", "title3"], default=None
    )
    parts: Optional[List[int]] = Field(
        alias="parts", examples=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], default=None
    )
    descendants: Optional[int] = Field(
        alias="descendants",
        examples=[1, 2, 3],
        default=None,
        description="Number of comments",
    )

    def __post_init__(self):
        if self.type == ItemType.JOB:
            assert self.url, "URL is required for a job"
        if self.type == ItemType.STORY:
            assert self.title, "Title is required for a story"
            assert self.url, "URL is required for a story"
        if self.type == ItemType.COMMENT:
            assert self.text, "Text is required for a comment"

    def __str__(self):
        return f"{self.title} by {self.by} ({self.url})"

    def is_story(self) -> bool:
        """
        Check if the item is a story
        """
        return self.type == ItemType.STORY

    def does_have_comments(self) -> bool:
        """
        Check if the item has comments
        """
        if self.type == ItemType.STORY:
            return self.descendants > 0
        return False


class User(BaseModel):
    """
    User class to represent a user from Hacker News
    """

    id: str = Field(alias="id", examples=["user1", "user2", "user3"])
    created: int = Field(alias="created", examples=[1615767531, 1615767532, 1615767533])
    karma: int = Field(alias="karma", examples=[1, 2, 3])
    about: Optional[str] = Field(
        alias="about", examples=["about1", "about2", "about3"], default=None
    )
    submitted: Optional[List[int]] = Field(
        alias="submitted", examples=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], default=None
    )


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
