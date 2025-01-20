from dotenv import load_dotenv
from pathlib import Path

import os


env_path = Path(__file__).resolve().parent.parent.parent / '.env'

load_dotenv(env_path)


HOST = os.getenv( 'HOST', 'localhost' )
PORT = int( os.getenv( 'PORT', 8080 ) )

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWItCH_CLIENT_SECRET = os.getenv('TWItCH_CLIENT_SECRET')
TWITCH_REDIRECT_URI = os.getenv('TWITCH_REDIRECT_URI')
TWITCH_OAUTH_URL = os.getenv('TWITCH_OAUTH_URL')
TWITCH_TOKEN_URL = os.getenv('TWITCH_TOKEN_URL')
TWITCH_API_URL = os.getenv('TWITCH_API_URL')

if  ( not YOUTUBE_API_KEY ) or      \
    ( not TWITCH_CLIENT_ID ) or     \
    ( not TWItCH_CLIENT_SECRET ) or \
    ( not TWITCH_REDIRECT_URI ) or  \
    ( not TWITCH_OAUTH_URL ) or     \
    ( not TWITCH_TOKEN_URL ) or     \
    ( not TWITCH_API_URL )          \
:
    raise Exception( 'Environment variable values are missing!' )
