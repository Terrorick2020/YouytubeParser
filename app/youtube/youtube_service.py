from fastapi import HTTPException
from googleapiclient.discovery import build
from dotenv import load_dotenv

from .fields.channel import *
from .fields.videos import *

import os


load_dotenv()

API_KEY = os.getenv('API_KEY')

if not API_KEY:
    raise Exception( 'Environment variable values are missing!' )

async def parse_youtube(parser_config):

    channel_name = parser_config.channelName.strip().replace('@', '')
    video_count = parser_config.videoCount

    youtube = build( 'youtube', 'v3', developerKey=API_KEY )

    if not youtube:
        raise HTTPException(
            status_code=500,
            detail='Youtube api crashed!',
        )

    channel_info = get_channel_info( channel_name, youtube )
    channel_id = get_channel_id( channel_info )
    channel_statistics = get_channel_statistics( channel_id, youtube )

    video_ids = get_video_ids( channel_id, youtube, video_count )
    video_stats = get_video_statistics( video_ids, youtube )

    result_info = {
        'channelID': channel_id,
        'channelName': channel_name,
        'channelStatistics': channel_statistics,
        'videoCount': video_count,
        'videoStatistics': video_stats,
    }

    return result_info
