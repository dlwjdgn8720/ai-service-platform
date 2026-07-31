from fastapi import FastAPI
from routers.hello import hello_router
from routers.todo import todo_router

app = FastAPI() # FastAPI 서버 생성

@app.get("/") #http://127.0.0.1:8000/
async def welcome() -> dict: #{ key: value ...}
    return {
        "message" : "welcome to FastAPI world!!"
    }

@app.post("/") #http://127.0.0.1:8000/
async def welcome() -> dict: #{ key: value ...}
    return {
        "message" : "welcome to FastAPI world!!"
    }

app.include_router(hello_router)
app.include_router(todo_router)

