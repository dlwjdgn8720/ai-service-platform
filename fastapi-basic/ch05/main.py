from fastapi import FastAPI
from routes.study import study_router

app = FastAPI()

app.include_router(study_router)