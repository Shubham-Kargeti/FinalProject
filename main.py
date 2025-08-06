from fastapi import FastAPI
import models
from database import engine
from routes import admin, claim, users

app = FastAPI()

app.include_router(admin.router)
app.include_router(users.router)
app.include_router(claim.router)

models.Base.metadata.create_all(bind=engine)





