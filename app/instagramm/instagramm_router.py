from fastapi import APIRouter

from . import instagramm_service


instagramm_router = APIRouter()

@instagramm_router.get(
    '/instagramm',
    tags=['Instagramm 🎬'],
    summary='Получить информацию профиля!'
)
async def instagramm_parser():
    parser_result = await instagramm_service.pars_instagramm()
    return parser_result
