from fastapi import HTTPException

from .utils.parser_utils import TwitchParserConfig


async def parse_twitch( parser_config: TwitchParserConfig ):
    result = {
        'message': 'В разработке!'
    }

    return result
