# ----------------------------------------------
#  도서 관리 애플리케이션 - CRUD
# ----------------------------------------------
from schemas.book_schema import Book, Book_Item, Books
from models.book_model import BookModel
from sqlalchemy.orm import Session
from sqlalchemy import select,delete
from fastapi import APIRouter, Path, HTTPException, status, Depends
from database import get_db

book_router = APIRouter()

# C: Insert
@book_router.post("/book" , response_model = Book,
                  status_code=status.HTTP_201_CREATED)
async def add_book(book_data: Book_Item,
                   db:Session = Depends(get_db)) -> dict:

    bookModel = BookModel(
        title = book_data.title,
        price = book_data.price,
        isbn =  book_data.isbn
    )

    db.add(bookModel) # SQL 생성 -> Insert into books values(?,?,?)
    db.commit() # DB에 SQL 전송 및 실행
    db.refresh(bookModel) # 실행 결과(title, price, isbn)받기

    return book_data

# R: Select All
@book_router.get("/books",
                  response_model=Books) #[{Book}, {Book} ...]
async def get_all(db: Session=Depends(get_db)):

    #DB_연동
    books = db.execute(
        select(BookModel).order_by(BookModel.id)
    ) # [{}, ...]
    result = books.scalars().all()

    return {
        "books": result
    }

# R: Select Id
@book_router.get("/book/{id}",
                response_model=Book)
async def get_id(id :int,
                  db: Session=Depends(get_db)) -> dict:
    book = db.get(BookModel, id) # Select 쿼리 생성, 전송 <--- DB

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id does not exist"
        )

    return book

# U: Update
@book_router.put("/book/{id}",
                    response_model=Book)
async def update(new_data:Book_Item, 
                 id: int = Path(...),
                 db: Session = Depends(get_db)) -> dict:
    book = db.get(BookModel, id)

    if book is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="Id does not exist"
        )

    book.title = new_data.title
    book.price = new_data.price
    book.isbn = new_data.isbn

    db.commit()
    db.refresh(book)
    
    return book

# D: Delete All
@book_router.delete("/books")
async def delete_all(db: Session = Depends(get_db)) -> dict:
    result = db.execute(delete(BookModel))
    db.commit()

    if result.rowcount == 0:
        return {
            "message": "도서가 존재하지 않습니다."
        }

    return {
        "message": "전체 데이터 삭제 완료!!"
    }

# D: Delete Id
@book_router.delete("/book/{id}")
async def delete_id(id: int, db: Session = Depends(get_db)) -> dict:
    book = db.get(BookModel, id)

    if book is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Id does not exist!!"
        )
    
    db.delete(book)
    db.commit()

    return {
        "message": "도서 삭제 완료"
    }