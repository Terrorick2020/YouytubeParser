from fastapi import FastAPI
import uvicorn

from config.main_config import HOST, PORT

from app.youtube.youtube_router import youtube_router
from app.hello.hello_router import hello_router


app = FastAPI()

app.include_router( hello_router )
app.include_router( youtube_router )

if __name__ == '__main__':
    try:
        uvicorn.run(
            'main:app',
            host = HOST,
            port = PORT,
            reload = True,
        )
    except Exception as error:
        print( error )
    finally:
        print( 'The server is stopped!' )
