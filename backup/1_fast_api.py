# 터미널에서 uvicorn app:app --reload --port 8000 실행
# 웹 브라우저에서 접속: http://localhost:8000/

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
