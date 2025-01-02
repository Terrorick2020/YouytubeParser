from fastapi import APIRouter
from . import vk_service


vk_router = APIRouter()

@vk_router.get(
    '/vk',
    tags=['Vk ⚡'],
    summary='Получить информацию группы / страницы!',
)
async def vk_parser():
    parser_result = await vk_service.parse_vk()
    return parser_result
