import requests
from fastapi import HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse

from config.main_config import TWITCH_OAUTH_URL, TWITCH_CLIENT_ID, \
                               TWITCH_REDIRECT_URI, TWITCH_TOKEN_URL, \
                               TWItCH_CLIENT_SECRET, TWITCH_API_URL

from .utils.parser_utils import TwitchParserConfig


async def home():
    redirect_url = "/twitch/login"

    return HTMLResponse(f'''
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Twitch App</title>
        </head>
        <body>
            <h1>Добро пожаловать в Twitch App</h1>
            <a href="{redirect_url}">
                <button>Войти с Twitch</button>
            </a>
        </body>
        </html>
    ''')

async def login():
    auth_url = f"{TWITCH_OAUTH_URL}?client_id={TWITCH_CLIENT_ID}&redirect_uri={TWITCH_REDIRECT_URI}&response_type=code&scope=user:read:email"
    return RedirectResponse(url=auth_url)

async def callback(code: str):
     # Запрашиваем токен от Twitch с полученным кодом
    token_response = requests.post(TWITCH_TOKEN_URL, data={
        'client_id': TWITCH_CLIENT_ID,
        'client_secret': TWItCH_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': TWITCH_REDIRECT_URI
    })

    token_data = token_response.json()
    access_token = token_data.get('access_token')

    if not access_token:
        raise HTTPException(status_code=400, detail="Unable to get access token")

    # Перенаправляем на страницу с данными пользователя
    return RedirectResponse(url=f"/twitch/parse-result?access_token={access_token}")

async def parse_twitch( access_token: str ):
    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }

    # Получаем информацию о пользователе
    user_response = requests.get(f"{TWITCH_API_URL}users", headers=headers)
    user_data = user_response.json()

    if not user_data.get('data'):
        raise HTTPException(status_code=400, detail="Unable to fetch user data")

    user = user_data['data'][0]

    # Получаем подписки канала
    subscriptions_response = requests.get(f"{TWITCH_API_URL}subscriptions?broadcaster_id={user['id']}", headers=headers)
    subscriptions = subscriptions_response.json()

    # Получаем данные о клипах
    clips_response = requests.get(f"{TWITCH_API_URL}clips?broadcaster_id={user['id']}", headers=headers)
    clips = clips_response.json()

    result = {
        "user": user,
        "subscriptions": subscriptions.get('data', []),
        "clips": clips.get('data', []),
    }

    return result
