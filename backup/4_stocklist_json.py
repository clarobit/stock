# # json으로 파일 읽기 기능 추가
# stocks.json 파일에 티커 목록을 저장 필요
# 예시
# { "us": ["AAPL"], "kr": ["005930.KS"], "jp": ["7203.T"] }




# 실행방법
# # 1. 서버 실행: 터미널에서
# uvicorn app:app --reload --port 8000

# # 2. 기본 확인 (브라우저)
# http://localhost:8000/

# # 3. local host로 현재가 조회 (브라우저 또는 터미널)
# 3-1) 특정 종목 확인
# http://localhost:8000/prices/AAPL
# 3-2) 특정 지역 확인
# http://localhost:8000/prices/kr
# 3-3) 전체 종목 확인
# http://localhost:8000/prices


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yfinance as yf
from pathlib import Path
import json

app = FastAPI()

# ---------- (필수) stocks.json에서 티커 읽기 ----------
# 기대 구조 예시:
# {
#   "us": ["AAPL", "MSFT", "NVDA"],
#   "kr": ["005930.KS", "000660.KS"]
# }
STOCKS_FILE = Path("stocks.json")


def load_stocks() -> dict:
    if not STOCKS_FILE.exists():
        STOCKS_FILE.write_text(json.dumps({"us": [], "kr": []}), encoding="utf-8")
    return json.loads(STOCKS_FILE.read_text(encoding="utf-8"))


# ---------- 기존 모델/엔드포인트 ----------
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


@app.get("/price/{ticker}")
def get_price(ticker: str):
    tk = yf.Ticker(ticker)
    hist = tk.history(period="1d", interval="1m")
    if hist.empty:
        return {"error": "no data"}
    last_price = hist["Close"].iloc[-1]
    return {"ticker": ticker.upper(), "price": float(last_price)}


# ---------- 추가: stocks.json에 등록된 티커들의 가격 조회 ----------
@app.get("/prices/{region}")
def get_prices_by_region(region: str):
    stocks = load_stocks()
    if region not in stocks:
        raise HTTPException(404, f"region not found. available regions: {list(stocks.keys())}")

    results = []
    for t in stocks[region]:
        tk = yf.Ticker(t)
        hist = tk.history(period="1d", interval="1m")

        # 회사 이름 가져오기
        try:
            name = tk.info.get("shortName")
        except Exception:
            name = None

        if hist.empty:
            results.append({"ticker": t, "name": name or t, "error": "no data"})
        else:
            last_price = float(hist["Close"].iloc[-1])
            results.append({"ticker": t, "name": name or t, "price": last_price})
    return {"region": region, "results": results}


@app.get("/prices/{region}")
def get_prices_by_region(region: str):
    stocks = load_stocks()
    if region not in stocks:
        raise HTTPException(
            404, f"region not found. available regions: {list(stocks.keys())}"
        )

    results = []
    for t in stocks[region]:
        tk = yf.Ticker(t)
        hist = tk.history(period="1d", interval="1m")

        # 회사 이름 가져오기
        try:
            name = tk.info.get("shortName")
        except Exception:
            name = None

        if hist.empty:
            results.append({"ticker": t, "name": name or t, "error": "no data"})
        else:
            last_price = float(hist["Close"].iloc[-1])
            results.append({"ticker": t, "name": name or t, "price": last_price})
    return {"region": region, "results": results}


@app.get("/prices")
def get_prices_all():
    stocks = load_stocks()
    all_results = {}
    for region, tickers in stocks.items():
        region_results = []
        for t in tickers:
            tk = yf.Ticker(t)
            hist = tk.history(period="1d", interval="1m")

            # 회사 이름 가져오기
            try:
                name = tk.info.get("shortName")
            except Exception:
                name = None

            if hist.empty:
                region_results.append(
                    {"ticker": t, "name": name or t, "error": "no data"}
                )
            else:
                last_price = float(hist["Close"].iloc[-1])
                region_results.append(
                    {"ticker": t, "name": name or t, "price": last_price}
                )
        all_results[region] = region_results
    return all_results
