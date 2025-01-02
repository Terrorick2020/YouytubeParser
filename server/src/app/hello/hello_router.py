from fastapi import APIRouter

from . import hello_service

hello_router = APIRouter()

@hello_router.get(
    '/',
    tags = ['Test server'],
    summary = 'Проверка работоспособности сервиса!',
    status_code = 200,
)
async def hello():
    result_hello = await hello_service.hello()
    return result_hello
