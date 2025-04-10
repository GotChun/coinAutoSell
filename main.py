# main.py

from config import ACCESS_KEY, SECRET_KEY
from utils import get_market_name_map,log_trade
from strategy import check_buy_condition, check_sell_condition
from upbit_api import place_market_buy, place_market_sell , get_krw_balance
import time

# 거래 가능 종목 리스트 불러오기 (예: KRW-BTC → 비트코인)
market_name_map = get_market_name_map()
tickers = list(market_name_map.keys())  # KRW 마켓 기준 전체 종목

holding_list = []  # 현재 보유 중인 종목 리스트

print("🔁 자동매매 시작...")

while True:
    qualified = []  # 조건에 맞는 종목 리스트
    traded_this_round = [] # 이번 회차에 거래 된 종목 리스트 

    for ticker in tickers:
        coin_name = market_name_map.get(ticker,ticker)
        print(f"\n📌 [매수 조건 검사 중: {coin_name}]")
        
        if ticker not in holding_list:  # 보유 중이지 않은 코인만 검색
            if check_buy_condition(ticker): # 조건 검사
                qualified.append(ticker) # 조건에 맞다면 리스트에 추가
        else:   # 보유중인 코인 매도 조건 확인
            # 매도 조건 체크
            if check_sell_condition(ticker):
                result = place_market_sell(ticker)  # 매도
                if result:
                    holding_list.remove(ticker) # 보유 중인 코인 리스트에서 제거
                    traded_this_round.append(f"{coin_name} (매도)")
                    time.sleep(5)

    if qualified:
        krw = get_krw_balance() # 조건에 맞는 코인이 있다면 재산 조회 후 거래
        if krw >= 5000:
            per_amount = (krw * 0.995) / len(qualified)
            print(f"\n✅ 조건 만족 종목 {len(qualified)}개 발견 → 개당 약 {int(per_amount)}원 매수")

            for ticker in qualified:
                coin_name = market_name_map.get(ticker,ticker)
                result = place_market_buy(ticker,per_amount)
                if result:
                    holding_list.append(ticker)
                    traded_this_round.append(f"{coin_name} (매수)")
                    time.sleep(5)
        else:
            print("❌ KRW 잔액 부족으로 매수 불가")
    else:
        print("🟨 조건 만족 종목 없음 → 매수 없음")

    # ✅ 순회 결과 출력
    print("\n✅ 전체 종목 순회 완료.")
    if traded_this_round:
        print("📊 이번 순회에서 거래된 종목:")
        for trade in traded_this_round:
            print(f" - {trade}")
    else:
        print("🟨 거래된 종목 없음.")

    print("\n⏳ 10분 후 다시 순회...\n")
    time.sleep(600)