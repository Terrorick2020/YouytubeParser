from pydantic import BaseModel


class YoutubeParserConfig( BaseModel ):
    channelName: str
    videoCount: int
