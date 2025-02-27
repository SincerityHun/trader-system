import pandas as pd
import ta


def preprocessData(df: pd.DataFrame) -> pd.DataFrame:
    """
    원시 OHLCV 데이터를 받아 기술적 지표를 추가하는 전처리 함수.

    Args:
        df (pd.DataFrame): OHLCV 데이터가 포함된 DataFrame.

    Returns:
        pd.DataFrame: EMA(130), MACD Histogram, Stochastic Oscillator, %b, MFI 등을 추가한 DataFrame.
    """

    # EMA 130 (지수 이동 평균)
    df["EMA_130"] = df["close"].ewm(span=130, adjust=False).mean()

    # MACD 및 Histogram (MACD 라인 차이)
    df["MACD"] = ta.trend.macd(df["close"])
    df["MACD_Signal"] = ta.trend.macd_signal(df["close"])
    df["MACD_Histogram"] = df["MACD"] - df["MACD_Signal"]

    # Stochastic Oscillator (%K, %D)
    df["Stochastic_%K"] = ta.momentum.stoch(
        df["high"], df["low"], df["close"], window=14, smooth_window=3
    )
    df["Stochastic_%D"] = df["Stochastic_%K"].rolling(3).mean()

    # Bollinger Bands %b 값
    df["%b"] = ta.volatility.bollinger_pband(df["close"], window=20, fillna=True)

    # Money Flow Index (MFI)
    df["MFI"] = ta.volume.money_flow_index(
        df["high"], df["low"], df["close"], df["volume"], window=14
    )

    # Stochastic RSI (과매수/과매도 확인용)
    df["Stoch_RSI"] = ta.momentum.stochrsi(df["close"], window=14)

    return df
