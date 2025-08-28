# ---------- 추가 기능 ----------
# # html 추가


# ---------- 설명 ----------
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

# app.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import yfinance as yf
import json

app = FastAPI()

# ---------- stocks.json ----------
STOCKS_FILE = Path("stocks.json")


def load_stocks() -> dict:
    if not STOCKS_FILE.exists():
        STOCKS_FILE.write_text(json.dumps({"us": [], "kr": []}), encoding="utf-8")
    return json.loads(STOCKS_FILE.read_text(encoding="utf-8"))


# ---------- 페이지 ----------
@app.get("/", response_class=FileResponse)
def page_root():
    return "static/index.html"


@app.get("/prices", response_class=FileResponse)
def page_prices():
    return "static/index.html"


INDEX_PAGES = {"stocks", "alerts", "dashboard"}


@app.get("/{page}", response_class=FileResponse)
def page_catch(page: str):
    if page in INDEX_PAGES:
        return "static/index.html"
    raise HTTPException(404, "Not Found")


# ---------- API (/api/...) ----------
# url에서 api는 백엔드용으로 구분하기 위해 사용
# ex) /api/price/{ticker} : 특정 종목 현재가 조회
class Alert(BaseModel):
    ticker: str
    operator: str
    target: float


@app.get("/api/price/{ticker}")
def api_get_price(ticker: str):
    tk = yf.Ticker(ticker)
    hist = tk.history(period="1d", interval="1m")
    try:
        info = tk.info
        name = info.get("shortName") or info.get("longName")
    except Exception:
        name = None
    if hist.empty:
        return {
            "ticker": ticker.upper(),
            "name": name or ticker.upper(),
            "error": "no data",
        }
    last_price = float(hist["Close"].iloc[-1])
    return {
        "ticker": ticker.upper(),
        "name": name or ticker.upper(),
        "price": last_price,
    }


@app.get("/api/prices/{region}")
def api_get_prices_by_region(region: str):
    stocks = load_stocks()
    if region not in stocks:
        raise HTTPException(
            404, f"region not found. available regions: {list(stocks.keys())}"
        )
    results = []
    for t in stocks[region]:
        tk = yf.Ticker(t)
        hist = tk.history(period="1d", interval="1m")
        try:
            info = tk.info
            name = info.get("shortName") or info.get("longName")
        except Exception:
            name = None
        if hist.empty:
            results.append({"ticker": t, "name": name or t, "error": "no data"})
        else:
            results.append(
                {"ticker": t, "name": name or t, "price": float(hist["Close"].iloc[-1])}
            )
    return {"region": region, "results": results}


@app.get("/api/prices")
def api_get_prices_all():
    stocks = load_stocks()
    all_results = {}
    for region, tickers in stocks.items():
        region_results = []
        for t in tickers:
            tk = yf.Ticker(t)
            hist = tk.history(period="1d", interval="1m")
            try:
                info = tk.info
                name = info.get("shortName") or info.get("longName")
            except Exception:
                name = None
            if hist.empty:
                region_results.append(
                    {"ticker": t, "name": name or t, "error": "no data"}
                )
            else:
                region_results.append(
                    {
                        "ticker": t,
                        "name": name or t,
                        "price": float(hist["Close"].iloc[-1]),
                    }
                )
        all_results[region] = region_results
    return all_results
