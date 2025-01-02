from pydantic import BaseModel


class ParserConfig( BaseModel ):
    channelName: str
    videoCount: int
