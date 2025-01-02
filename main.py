from fastapi import FastAPI
import uvicorn

from app.youtube.youtube_router import youtube_router


app = FastAPI()

app.include_router( youtube_router, prefix='/api' )

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
