# fast api + pydantic 사용 예제
# 터미널에서 uvicorn app:app --reload --port 8000
# 웹 브라우저에서 접속: http://localhost:8000/

# 다른 터미널에서 리턴 확인
# 아래 curl 명령어로 POST 요청 후 리턴 확인
# curl -X POST http://localhost:8000/alerts \
#   -H "Content-Type: application/json" \
#   -d '{"ticker":"AAPL","operator":">=","target":200}'

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 1) Pydantic 모델 정의
class Alert(BaseModel):
    ticker: str
    operator: str
    target: float

# 2) POST 요청으로 Alert 등록 받기
@app.post("/alerts")
def create_alert(alert: Alert):
    # 실제로는 DB나 메모리에 저장해야 함 (지금은 테스트라 그대로 반환)
    return {"status": "ok", "data": alert}

# 3) 기본 라우트
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
