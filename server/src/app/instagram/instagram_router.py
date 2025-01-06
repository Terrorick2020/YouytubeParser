from fastapi import APIRouter

from .utils.parser_utils import InstagramParserConfig
from . import instagram_service


instagram_router = APIRouter()

@instagram_router.post(
    '/instagram',
    tags = [ 'Instagram 🌷͙֒ ' ],
    summary = 'Получить информацию о профиле!',
    status_code = 200,
)
async def instagram_parser( parser_config: InstagramParserConfig ):

    if parser_config.hasBusinessProfile:
        parser_result = await instagram_service.parse_instagram_with( parser_config )
    else:
        parser_result = await instagram_service.parse_instagram_without( parser_config )

    return parser_result
