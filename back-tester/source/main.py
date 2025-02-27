from dataCollector import getData
from dataPreprocessor import preprocessData
from config import dataConfig
from strategyModel import customTradingStrategy
from backTester import backtest
from drawer import drawGraph
import logging

# Log 설정
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    logging.info("Step 1: 데이터 설정을 가져오는 중...")
    curDataConfig = dataConfig
    logging.info(f"Step 2: 데이터 가져오기 시작 (Symbol: {curDataConfig.symbol}, Timeframe: {curDataConfig.timeframe})")
    df = getData(curDataConfig)
    df = preprocessData(df)
    logging.info("Step 3: 전략 적용 중...")
    df = customTradingStrategy(df)
    logging.info("Step 4: 백테스트 실행 중...")
    return_pct,trade_history = backtest(df)
    logging.info("Step 6: 그래프 그리기 시작...")
    drawGraph(df,trade_history)


if __name__ == "__main__":
    main()
