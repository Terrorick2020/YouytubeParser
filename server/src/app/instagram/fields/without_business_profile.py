import instaloader
import datetime
import time


# 1. Получение подписчиков
def get_followers_count( profile ):
    return profile.followers

# 2. Среднее количество лайков за последние N постов
def get_average_likes(last_n_posts):
    likes_total = 0
    for post in last_n_posts:
        likes_total += post.likes
    return likes_total / len(last_n_posts) if last_n_posts else 0

# 3. Вовлеченность (реакции + комментарии) / публикации
def calculate_engagement(last_n_posts):
    total_reactions = 0
    total_comments = 0
    total_views = 0  # Если доступны просмотры видео
    for post in last_n_posts:
        total_reactions += post.likes
        total_comments += post.comments
        if post.is_video and post.video_view_count:
            total_views += post.video_view_count
    total_posts = len(last_n_posts)
    if total_posts == 0:
        return 0
    engagement = ((total_reactions + total_comments) / total_posts) / (total_views if total_views else 1) * 100
    return engagement

# 4. Количество публикаций
def get_total_posts( profile ):
    return profile.mediacount

# 5. Средняя частота публикаций за последние 30 дней
def get_posts_frequency( profile ):
    now = datetime.datetime.now()
    thirty_days_ago = now - datetime.timedelta(days=30)
    
    # Получаем публикации за последние 30 дней
    posts_in_last_30_days = []
    for post in profile.get_posts():
        if post.date_utc > thirty_days_ago:
            posts_in_last_30_days.append(post)
    
    return len(posts_in_last_30_days) / 30 if posts_in_last_30_days else 0

# 6. Безопасное получение публикаций с задержкой
def safe_get_posts(profile, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            return list(profile.get_posts())
        except instaloader.exceptions.ConnectionException:
            retries += 1
            print(f"Connection error, retrying... ({retries}/{max_retries})")
            time.sleep(20)  # Пауза на 20 секунд при ошибке
    return []
