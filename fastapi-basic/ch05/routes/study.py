import joblib
import pandas as pd

from fastapi import APIRouter
from schemas.study import Study

study_router = APIRouter()

# 1. 모델 호출
model = joblib.load("models/model.pkl")

@study_router.post("/predict")    # 공부시간 ==> 점수 예측(?)
async def study_predict(features: Study) -> dict:
    # 2. Pydantic -> dict 타입 변경
    data = features.model_dump()    # {"study_hour": 3}

    # 3. dict -> DataFrame 
    df = pd.DataFrame([data]) # dict 항목이 1개이면 반드시 [] 리스트형식 처리해야함!!

    # 4. predict 실행 => predict 결과는 리스트(배열) 형태로 반환됨
    prediction = model.predict(df)[0] 

    return {
        "predict_score": round(prediction[0], 2)
    }