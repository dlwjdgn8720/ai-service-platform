from fastapi import FastAPI
from routes.book import router
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware


# 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 허용할 프론트엔드 주소 목록 (테스트 시에는 ["*"]로 모든 도메인 허용 가능)
origins = [
    "http://localhost:5173",      # 리액트 기본 포트 예시
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # 모든 도메인을 허용하려면 ["*"]
    allow_credentials=True,
    allow_methods=["*"],             # OPTIONS를 포함한 모든 HTTP 메서드 허용
    allow_headers=["*"],             # 모든 HTTP 헤더 허용
)

app.include_router(router, prefix="/fastapi")

