def get_channel_info( username, youtube ):
    request = youtube.search().list(
        part='snippet',
        q=username,
        type='channel'
    )
    response = request.execute()

    if not response['items']:
        raise Exception( 'Request error in "get_channel_info"!' )

    return response['items'][0]

def get_channel_id( channel_info ):

    if not channel_info:
        raise Exception( 'Don`t have a channel info!' ) 

    return channel_info['id']['channelId']

def get_channel_statistics( channel_id, youtube ):
    request = youtube.channels().list(
        part="statistics",
        id=channel_id
    )
    response = request.execute()

    if not response['items']:
        raise Exception( 'Request error in "get_channel_statistics"!' )

    stats = response['items'][0]['statistics']
    view_count = stats.get( 'viewCount', 'Не доступно' )
    subscriber_count = stats.get(' subscriberCount', 'Не доступно' )
    video_count = stats.get( 'videoCount', 'Не доступно' )

    channel_stats = {
        'viewCount': view_count,
        'subscriberCount': subscriber_count,
        'videoCount': video_count,
    }

    return channel_stats
