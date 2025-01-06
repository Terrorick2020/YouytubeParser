from pydantic import BaseModel
from typing import Optional


class InstagramParserConfig( BaseModel ):
    profileName: str
    coveragePostsCount: int
    postsCount: int
    hasBusinessProfile: bool

    userId: Optional[str] = None
    instagramAccessToken: Optional[str] = None
