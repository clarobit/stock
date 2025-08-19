from fastapi import FastAPI
from pydantic import BaseModel
import yfinance as yf

app = FastAPI()


# Pydantic 모델
class Alert(BaseModel):
    ticker: str
    operator: str
    target: float


@app.post("/alerts")
def create_alert(alert: Alert):
    return {"status": "ok", "data": alert}


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


# yfinance 테스트용 엔드포인트
@app.get("/price/{ticker}")
def get_price(ticker: str):
    tk = yf.Ticker(ticker)
    hist = tk.history(period="1d", interval="1m")  # 오늘 데이터
    if hist.empty:
        return {"error": "no data"}
    last_price = hist["Close"].iloc[-1]
    return {"ticker": ticker.upper(), "price": float(last_price)}

# # fastapi + pydantic + yfinance 사용 예제
# # 서버 실행: 터미널에서
# uvicorn app:app --reload --port 8000

# # 기본 확인 (브라우저)
# http://localhost:8000/

# # POST 테스트 (다른 터미널)
# curl -X POST http://localhost:8000/alerts \
#   -H "Content-Type: application/json" \
#   -d '{"ticker":"AAPL","operator":">=","target":200}'

# # yfinance로 현재가 조회 (브라우저 또는 터미널)
# http://localhost:8000/price/AAPL
# # 또는
# curl http://localhost:8000/price/AAPL
