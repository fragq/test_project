from fastapi import FastAPI
from app.api import router
from app.db import lifespan


app = FastAPI(lifespan=lifespan)

app.include_router(router)
