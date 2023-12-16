from fastapi import FastAPI
from api.base_router import base_router
from db.db import engine, Base
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(base_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    # create db tables
    from models.user_model import User
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get('/ping/')
async def healthcheck():
    return {"ping": "pong!"}
