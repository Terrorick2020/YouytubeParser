from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

INSTAGRAM_APP_ID = 'your_instagram_app_id'
INSTAGRAM_APP_SECRET = 'your_instagram_app_secret'
INSTAGRAM_REDIRECT_URI = 'http://localhost:8000/auth/facebook/callback'
FB_APP_ID = 'your_facebook_app_id'
FB_APP_SECRET = 'your_facebook_app_secret'

# Настройки из .env файла
INSTAGRAM_APP_ID = os.getenv("INSTAGRAM_APP_ID")
INSTAGRAM_APP_SECRET = os.getenv("INSTAGRAM_APP_SECRET")
INSTAGRAM_REDIRECT_URI = os.getenv("INSTAGRAM_REDIRECT_URI")
FB_APP_ID = os.getenv("FB_APP_ID")
FB_APP_SECRET = os.getenv("FB_APP_SECRET")

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Модели данных
class InstagramData(BaseModel):
    followers_count: int
    unique_impressions: int
    average_likes: float
    engagement_rate: float
    total_posts: int
    avg_post_frequency: float


# Функция для получения access token
def get_instagram_access_token(fb_access_token: str):
    url = f"https://graph.facebook.com/v12.0/me?fields=instagram_business_account&access_token={fb_access_token}"
    response = requests.get(url)
    data = response.json()
    if "instagram_business_account" not in data:
        raise HTTPException(status_code=400, detail="Instagram business account not found")
    instagram_account_id = data["instagram_business_account"]["id"]

    # Получаем long-lived token для Instagram
    url = f"https://graph.facebook.com/v12.0/{instagram_account_id}?fields=access_token&access_token={fb_access_token}"
    response = requests.get(url)
    data = response.json()
    return data["access_token"]

# Функция для получения данных пользователя из Instagram Graph API
def get_instagram_data(instagram_access_token: str):
    url = f"https://graph.instagram.com/me/media?fields=id,caption,like_count,comments_count,media_type,media_url,thumbnail_url,timestamp&access_token={instagram_access_token}"
    response = requests.get(url)
    media_data = response.json()
    if 'data' not in media_data:
        raise HTTPException(status_code=400, detail="Error fetching Instagram data")

    # Получаем статистику по подписчикам и охвату
    followers_url = f"https://graph.instagram.com/me?fields=followers_count,impressions&access_token={instagram_access_token}"
    followers_response = requests.get(followers_url)
    followers_data = followers_response.json()

    followers_count = followers_data.get('followers_count', 0)
    unique_impressions = followers_data.get('impressions', 0)

    # Статистика по постам
    posts = media_data['data']
    total_likes = 0
    total_comments = 0
    total_views = 0
    for post in posts:
        total_likes += post.get('like_count', 0)
        total_comments += post.get('comments_count', 0)
        total_views += post.get('media_type', 0)

    avg_likes_per_post = total_likes / len(posts) if posts else 0
    engagement_rate = ((total_likes + total_comments) / total_views) * 100 if total_views else 0

    # Средняя частота публикаций
    avg_post_frequency = len(posts) / 30.0  # публикации за последние 30 дней

    return InstagramData(
        followers_count=followers_count,
        unique_impressions=unique_impressions,
        average_likes=avg_likes_per_post,
        engagement_rate=engagement_rate,
        total_posts=len(posts),
        avg_post_frequency=avg_post_frequency,
    )


# Эндпоинт для авторизации через Facebook
@app.get("/auth/facebook")
async def facebook_auth():
    url = f"https://www.facebook.com/v12.0/dialog/oauth?client_id={FB_APP_ID}&redirect_uri={INSTAGRAM_REDIRECT_URI}&scope=instagram_basic,ads_management,pages_show_list"
    return {"auth_url": url}

# Эндпоинт для получения токена и Instagram данных
@app.get("/auth/facebook/callback")
async def facebook_callback(code: str):
    # Получаем access token Facebook
    url = f"https://graph.facebook.com/v12.0/oauth/access_token?client_id={FB_APP_ID}&redirect_uri={INSTAGRAM_REDIRECT_URI}&client_secret={FB_APP_SECRET}&code={code}"
    response = requests.get(url)
    fb_data = response.json()

    if "access_token" not in fb_data:
        raise HTTPException(status_code=400, detail="Facebook access token not found")

    fb_access_token = fb_data["access_token"]
    instagram_access_token = get_instagram_access_token(fb_access_token)
    
    # Получаем Instagram данные
    instagram_data = get_instagram_data(instagram_access_token)
    return instagram_data

# Запуск сервиса
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)