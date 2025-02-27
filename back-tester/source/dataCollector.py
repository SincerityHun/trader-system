import pandas as pd
from config import DataConfig
import time

def getData(dataConfig: DataConfig):
    """
    거래소에서 OHLCV 데이터를 가져오는 함수.

    Args:
        dataConfig (DataConfig): 거래소, 심볼, 타임프레임 등의 정보를 담은 설정 객체.

    Returns:
        pd.DataFrame: OHLCV 데이터가 포함된 DataFrame.
    """
    all_data = []
    since = dataConfig.since  # 시작 시간 (None이면 최신 데이터부터)
    batch_size = 1000  # 바이낸스의 1회 요청 최대 개수
    ohlcv = dataConfig.exchange.fetch_ohlcv(dataConfig.symbol, dataConfig.timeframe, since=since, limit=batch_size)
    all_data.extend(ohlcv)
    while True:
        # 데이터 가져오기
        since = ohlcv[-1][0]
        ohlcv = dataConfig.exchange.fetch_ohlcv(dataConfig.symbol, dataConfig.timeframe, since=since, limit=batch_size)
        all_data.extend(ohlcv)
        if len(ohlcv)!= 1000:
            print("No more data available.")
            break
        time.sleep(0.5)  # 거래소 API 요청 제한을 피하기 위해 대기

    # 데이터프레임 변환
    df = pd.DataFrame(
        all_data, columns=["timestamp", "open", "high", "low", "close", "volume"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df
