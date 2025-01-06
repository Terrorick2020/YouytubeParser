from fastapi import APIRouter

from .utils.parser_utils import TwitchParserConfig
from . import twitch_service


twitch_router = APIRouter()

@twitch_router.post(
    '/twitch',
    tags = ['Twitch 🦋'],
    summary = 'Получение информации с канала!',
    status_code = 200,
)
async def twitch_parser( parser_config: TwitchParserConfig ):
    parser_result = await twitch_service.parse_twitch( parser_config )
    return parser_result