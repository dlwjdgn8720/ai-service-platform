# ----------------------------------------------
#  도서 관리 애플리케이션 - CRUD
# ----------------------------------------------
from schemas.book import BookItem, Book, Books
from models.book import BookModel
from sqlalchemy.orm import Session
from sqlalchemy import select,delete
from fastapi import APIRouter, Path, HTTPException, status, Depends
from database import get_db

router = APIRouter()

# Middleware


# C: Insert
@router.post("/book", response_model=Book)
async def addbook(bookItem: BookItem,
                   db: Session = Depends(get_db)) -> dict:

    # BookModel 생성 및 입력 데이터 추가
    bookModel = BookModel(
        title = bookItem.title,
        author = bookItem.author,
        publisher =  bookItem.publisher,
        year =  bookItem.year,
        status =  bookItem.status
    )

    # SQL 생성 -> Insert into books values(?,?,?)
    db.add(bookModel) 

    # DB에 SQL 전송 및 Transaction 실행
    db.commit() 

    # 실행 결과 가져오기
    db.refresh(bookModel) 

    return bookModel

# R: Select All
@router.get("/books", response_model= Books)          
async def getAll(db: Session=Depends(get_db)) -> list:

    #DB_연동
    init_books = db.execute(
        select(BookModel).order_by(BookModel.id)
    )
    books = init_books.scalars().all() #[{id: 1 ....}, {}....]

    return {
        "books": books
    }

# # R: Select Id
# @router.get("/book/{id}",
#                 response_model=Book)
# async def get_id(id :int,
#                   db: Session=Depends(get_db)) -> dict:
#     book = db.get(BookModel, id) # Select 쿼리 생성, 전송 <--- DB

#     if book is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Id does not exist"
#         )

#     return book

# # U: Update
@router.put("/book/{id}")
async def update(new_data:BookItem, 
                 id: int = Path(...),
                 db: Session = Depends(get_db)) -> dict:
    book = db.get(BookModel, id)

    if book is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="Id does not exist"
        )

    book.title = new_data.title
    book.author = new_data.author
    book.publisher = new_data.publisher
    book.year = new_data.year
    book.status = new_data.status

    db.commit()
    db.refresh(book)
    
    return {
        "isUpdate": True
    }

# # D: Delete All
# @router.delete("/books")
# async def delete_all(db: Session = Depends(get_db)) -> dict:
#     result = db.execute(delete(BookModel))
#     db.commit()

#     if result.rowcount == 0:
#         return {
#             "message": "도서가 존재하지 않습니다."
#         }

#     return {
#         "message": "전체 데이터 삭제 완료!!"
#     }

# # D: Delete Id
@router.delete("/book/{id}")
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
        "isDelete" : True
    }