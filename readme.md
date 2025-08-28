# 바이브 코딩으로 하는 주식 알람 웹 서비스

# 08/20
1. 가상환경 생성 및 라이브러리 설치   
```bash
pip install fastapi uvicorn yfinance pydantic
```
2. 야후 finance에서 주식 정보 불러와서 읽기 기능 추가
```bash
http://localhost:8000/price/AAPL
```

# 08/25
1. 주식 리스트.json파일 추가 후 주식 정보 확인
2. 국가별 구별 추가
3. 이름 확인 가능

<details>
<summary>실행 방법</summary>

```bash
# 1. 서버 실행: 터미널에서
uvicorn app:app --reload --port 8000

# 2. 기본 확인 (브라우저)
http://localhost:8000/

# 3. local host로 현재가 조회 (브라우저 또는 터미널)
# 3-1) 특정 종목 확인
http://localhost:8000/prices/AAPL
# 3-2) 특정 지역 확인
http://localhost:8000/prices/kr
# 3-3) 전체 종목 확인
http://localhost:8000/prices
```
</details>


# 08/28
1. html 파일 추가
2. html을 통해 페이지 이동 가능
