from dotenv import load_dotenv

import os

load_dotenv()


YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

if not YOUTUBE_API_KEY:
    raise Exception( 'Environment variable values are missing!' )