from fastapi import APIRouter

from .utils.parser_utils import TwitchParserConfig
from . import twitch_service


twitch_router = APIRouter()


@twitch_router.get(
    "/",
    tags = ['Twitch 🦋'],
    summary = 'Отправная точка для авторизации! (Домашня сраница)',
    status_code = 200,
)
async def home():
    home_result = await twitch_service.home()
    return home_result

@twitch_router.get(
    "/login",
    tags = ['Twitch 🦋'],
    summary = 'Роут для начала аутентификации (OAuth)',
    status_code = 200,
)
async def login():
    login_result = await twitch_service.login()
    return login_result

@twitch_router.get(
    "/callback",
    tags = ['Twitch 🦋'],
    summary = 'Обработка колбэка после авторизации (получение access_token)',
    status_code = 200,
)
async def callback( code: str ):
    callback_result = await twitch_service.callback( code )
    return callback_result

@twitch_router.get(
    '/parse-result',
    tags = ['Twitch 🦋'],
    summary = 'Получение информации с канала: подписчики, просмотры и лайки!',
    status_code = 200,
)
async def twitch_parser( access_token: str ):
    parser_result = await twitch_service.parse_twitch( access_token )
    return parser_result
