from fastapi import HTTPException
import instaloader

from .fields.with_business_profile import *
from .fields.without_business_profile import *
from .utils.parser_utils import InstagramParserConfig


async def parse_instagram_without( parser_config: InstagramParserConfig ):

    L = instaloader.Instaloader()
    profile_name = parser_config.profileName
    profile = instaloader.Profile.from_username( L.context, profile_name )

    followers = get_followers_count( profile )

    n_posts = parser_config.postsCount
    last_n_posts = safe_get_posts( profile )[:n_posts]
    
    average_likes = get_average_likes( last_n_posts )
    engagement = calculate_engagement( last_n_posts )

    total_posts = get_total_posts( profile )

    post_frequency = get_posts_frequency( profile )

    result = {
        'followers': followers,
        'average_likes': average_likes,
        'engagement': engagement,
        'total_posts': total_posts,
        'post_frequency': post_frequency,
        'message': 'success',
    }

    return result

async def parse_instagram_with( parser_config: InstagramParserConfig ):
    result = {
        'message': 'В разработке!'
    }

    return result