from typing import Literal
import ccxt


class DataConfig:
    def __init__(
        self,
        exchange: ccxt.Exchange,
        symbol: str,
        timeframe: Literal["1m", "5m", "15m", "1h", "4h", "1d"],
        limit: int,
        since=None,
    ):
        """
        데이터 설정을 위한 구성 클래스
        Args:
            exchange (ccxt.Exchange): CCXT 라이브러리를 사용한 거래소 객체
            symbol (str): 거래할 코인 심볼 (예: "BTC/USDT")
            timeframe (Literal["1m", "5m", "15m", "1h", "4h", "1d"]): 캔들 차트의 시간 간격
            limit (int): 가져올 데이터 개수 (예: 최근 1000개의 캔들 데이터)
            since (Optional[int]): 특정 시점 이후 데이터 가져오기 (Unix timestamp, 밀리초 단위)
        """
        self.exchange = exchange
        self.symbol = symbol
        self.timeframe = timeframe
        self.limit = limit
        self.since = since


# dataConfig = DataConfig(ccxt.binance(),"BTC/USDT","1h",100000)
# dataConfig = DataConfig(
#     ccxt.binance(),
#     "ETH/USDT",
#     "1h",
#     5000,
#     since=ccxt.binance().parse8601("2024-02-27 00:00:00"),
# )

dataConfig = DataConfig(
    ccxt.binance(),
    "ETH/USDT",
    "1h",
    360,
)
