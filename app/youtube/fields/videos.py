def get_video_ids( channel_id, youtube, max_results=10 ):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=max_results,
        order="date"
    )
    response = request.execute()

    video_ids = [item['id']['videoId'] for item in response['items'] if item['id']['kind'] == 'youtube#video']
    return video_ids

def get_video_statistics( video_ids, youtube ):
    all_video_stats = {}
    request = youtube.videos().list(
        part="statistics,contentDetails",
        id=','.join( video_ids )
    )
    response = request.execute()

    request_titles = youtube.videos().list(
        part="snippet",
        id=','.join(video_ids)
    )
    response_titles = request_titles.execute()

    video_titles = {item['id']: item['snippet']['title'] for item in response_titles['items']}

    all_video_stats = []
    total_views = 0
    total_videos = len( video_ids )

    for item in response['items']:
        video_id = item['id']
        title = video_titles.get( video_id, 'Unknown Title' )
        views = item['statistics'].get( 'viewCount', 0 )
        likes = item['statistics'].get( 'likeCount', 0 )
        comments = item['statistics'].get( 'commentCount', 0 )
        avg_view_duration = item['contentDetails'].get( 'duration', 'Не доступно' )

        engagement = ( int( likes ) + int( comments ) ) / int( views ) if views != 0 else 0
        total_views += int( views )

        all_video_stats.append({
            'ID': video_id,
            'title': title,
            'viewCount': views,
            'likeCount': likes,
            'commentCount': comments,
            'average_view_duration': avg_view_duration,
            'engagement': engagement,
        })
    
    average_views = total_views / total_videos if total_videos > 0 else 0

    result = {
        'averageViews': average_views,
        'videoStatisticsList': all_video_stats,
    }

    return result
