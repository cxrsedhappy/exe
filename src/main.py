import uvicorn
import contextlib

from fastapi import FastAPI

from session import global_init
from src.routes import user, post


@contextlib.asynccontextmanager
async def lifespan(application: FastAPI):
    await global_init()
    yield
    print('Shutdown')


app = FastAPI(title="exe", version="0.0.1", lifespan=lifespan)
app.include_router(user.router)
app.include_router(post.router)


if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
