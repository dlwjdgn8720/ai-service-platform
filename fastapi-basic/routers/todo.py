# /todo -get(R), post(C), put(U), delete(D)
from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path

todo_router = APIRouter()

# Item model
class Item(BaseModel):
    item: str
    status: str

# Todo model
class Todo(BaseModel):
    id: int
    item: Item

# Todo list
todo_list = []

# C: Create
@todo_router.post("/todo") #http://127.0.0.1:8000/
async def create_todo(todo: Todo) -> dict: #{ key: value ...}
    todo_list.append(todo)
    return {
        "message" : "create!!",
        "todo_list": todo_list
    }

# R: Read
@todo_router.get("/todo/all") #http://127.0.0.1:8000/
async def read_todo() -> dict: #{ key: value ...}
    return {
        "message::All" : "todo_list"
    }

# R: Read - id별 조회
@todo_router.get("/todo/{id}") #http://127.0.0.1:8000/
async def read_todo(id: int) -> dict: #{ key: value ...}
    for todo in todo_list:
        if todo.id == id:
            return {
                "todo": todo
            }
    return {
        "message" : "read todolist"
    }

# U: Update
@todo_router.put("/todo/{id}") #http://127.0.0.1:8000/
async def update_todo(update_item:Item, id:int = Path(..., title="id")) -> dict: #{ key: value ...}
    # for
    for todo in todo_list:
        #if
        if todo.id ==id:
            todo.item = update_item
            return {"message": "update 성공"}
    return {
        "message" : "id 확인!!",
    }

# D: Delete - all
@todo_router.delete("/todo") #http://127.0.0.1:8000/
async def delete_todo(id: int) -> dict: #{ key: value ...}
        if len(todo_list) > 0:
            todo_list.clear()
            return{"message": "삭제 성공!!"}
        return {
            "message": "데이터 없음!!"
        }

# D: Delete - id별
@todo_router.delete("/todo/{id}") #http://127.0.0.1:8000/
async def delete_todo(id: int) -> dict: #{ key: value ...}
     # for
        for index in range(len(todo_list)):
            todo = todo_list[index]
            #if
            if todo.id ==id:
                todo_list.pop(index)
                return{"message": "삭제 성공!!"}
        return {
            "message" : "id 확인!!"
        }

