from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn

from app.youtube.youtube_router import youtube_router
from app.vk.vk_router import vk_router


load_dotenv()

app = FastAPI()

app.include_router( youtube_router, prefix='/api' )
app.include_router( vk_router, prefix='/api' )

if __name__ == '__main__':
    try:
        uvicorn.run(
            'main:app',
            reload=True,
        )
    except Exception as error:
        print( error )
    finally:
        print( 'The server is stopped!' )
