from dotenv import load_dotenv
from pathlib import Path

import os


env_path = Path(__file__).resolve().parent.parent.parent / '.env'

load_dotenv(env_path)

HOST = os.getenv( 'HOST', 'localhost' )
PORT = int( os.getenv( 'PORT', 8080 ) )
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

if not YOUTUBE_API_KEY:
    raise Exception( 'Environment variable values are missing!' )
