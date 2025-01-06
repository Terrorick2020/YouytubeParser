from pydantic import BaseModel


class TwitchParserConfig( BaseModel ):
    channelName: str
    videoCount: int
