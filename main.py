# main.py

from config import ACCESS_KEY, SECRET_KEY
from utils import get_market_name_map,log_trade
from strategy import check_buy_condition, check_sell_condition
from upbit_api import place_market_buy, place_market_sell
import time

# 거래 가능 종목 리스트 불러오기 (예: KRW-BTC → 비트코인)
market_name_map = get_market_name_map()
tickers = list(market_name_map.keys())  # KRW 마켓 기준 전체 종목

holding_list = []  # 현재 보유 중인 종목 리스트

print("🔁 자동매매 시작...")

while True:
    traded_this_round = []
    for ticker in tickers:
        coin_name = market_name_map.get(ticker,ticker)
        print(f"\n📌 [체크 중: {coin_name}]")
        
        if ticker not in holding_list:
            # 매수 조건 체크
            if check_buy_condition(ticker):
                result = place_market_buy(ticker)
                if result:
                    holding_list.append(ticker)
                    traded_this_round.append(f"{coin_name} (매수)")
                    print(f"🟢 {coin_name} 매수 완료 → 보유 리스트에 추가")
                    time.sleep(5)
        else:
            # 매도 조건 체크
            if check_sell_condition(ticker):
                result = place_market_sell(ticker)
                if result:
                    holding_list.remove(ticker)
                    traded_this_round.append(f"{coin_name} (매도)")
                    print(f"🔴 {coin_name} 매도 완료 → 보유 리스트에서 제거")
                    time.sleep(5)
                    
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