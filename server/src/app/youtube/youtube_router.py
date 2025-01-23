from fastapi import APIRouter

from .utils.parser_utils import YoutubeParserConfig
from . import youtube_service


youtube_router = APIRouter()

@youtube_router.post(
    '/parse',
    tags = ['YouTube ▶️'],
    summary = 'Получить информацию канала!',
    status_code = 200,
)
async def youtube_parser( parser_config: YoutubeParserConfig ):
    parser_result = await youtube_service.parse_youtube( parser_config )
    return parser_result
