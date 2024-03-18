import asyncio
import uvicorn
import db.tables

from fastapi import FastAPI
from db.session import global_init

app = FastAPI(title="exe", version="0.0.1")

if __name__ == '__main__':
    asyncio.run(global_init())
    uvicorn.run('main:app')
