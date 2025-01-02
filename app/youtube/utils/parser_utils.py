from pydantic import BaseModel
from typing import Optional


class ParserConfig( BaseModel ):
    channelName: str
    videoCount: int
