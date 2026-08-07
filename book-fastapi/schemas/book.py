from pydantic import BaseModel, ConfigDict, Field
from typing import List

# post 메소드 호출시 매핑되는 모델
class BookItem(BaseModel):
    title: str
    author: str
    publisher: str
    year: str
    status: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "FastAPI",
                    "author": "홍길동",
                    "publisher": "파이썬 출반사",
                    "year": "2026",
                    "status": "대여가능"
                }
            ]
        }
    )

class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    year: str
    status: str

# Books 클래스 정의
class Books(BaseModel):
    books: List[Book] = Field(default_factory=False)