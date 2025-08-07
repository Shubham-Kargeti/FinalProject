from fastapi import FastAPI
from database import engine
from routes import admin, claim, users, auth
from contextlib import asynccontextmanager
from models import Base
from fastapi.middleware.cors import CORSMiddleware
from middleware.logger import log_requests


# models.Base.metadata.create_all(bind=engine)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Async DB table creation
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.middleware("http")(log_requests)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(users.router)
app.include_router(claim.router)
app.include_router(auth.router)



