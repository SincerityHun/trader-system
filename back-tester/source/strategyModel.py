import numpy as np

def movingAverageStrategy(df, short_window=10, long_window=50):
    df["short_ma"] = df["close"].rolling(short_window).mean()
    df["long_ma"] = df["close"].rolling(long_window).mean()

    df["signal"] = 0
    df.loc[df["short_ma"] > df["long_ma"], "signal"] = 1  # 매수
    df.loc[df["short_ma"] <= df["long_ma"], "signal"] = -1  # 매도

    return df


def customTradingStrategy(df, k_percent=0.5):
    """
    주어진 데이터프레임(df)에 3가지 트레이딩 전략을 적용하여 매수/매도 신호를 생성.

    Args:
        df (pd.DataFrame): OHLCV 데이터 및 기술 지표 포함
        k_percent (float): 변동성 돌파 전략의 K% 값 (기본값 0.5)

    Returns:
        pd.DataFrame: 'signal' 컬럼이 추가된 데이터프레임 (매수: 1, 매도: -1, 유지: 0)
    """

    # 매수/매도 신호 초기화
    df["signal"] = 0

    ### 전략 1: Triple Screen Trading System
    triple_screen_buy = (
        (df["EMA_130"].diff() > 0)
        & (df["MACD_Histogram"] > 0)
        & (df["Stochastic_%D"] < 30)
    )
    triple_screen_sell = (
        (df["EMA_130"].diff() < 0)
        & (df["MACD_Histogram"] < 0)
        & (df["Stochastic_%D"] > 70)
    )

    ### 📌 전략 2: 변동성 돌파 전략
    prev_high = df["high"].shift(1)
    prev_low = df["low"].shift(1)
    breakout_level = (
        prev_high + (prev_high - prev_low) * k_percent
    )  # 전일 가격 범위 * K%
    volatility_buy = df["close"] > breakout_level  # 변동성 돌파 매수
    volatility_sell = df.index == df.index[-1]  # 장 마감 시 매도

    ### 📌 전략 3: 추세 추종 전략
    trend_following_buy = (df["%b"] > 0.8) & (df["MFI"] > 80)
    trend_following_sell = (df["%b"] < 0.2) & (df["MFI"] < 20)

    # 각 전략의 신호를 통합하여 최종 매수/매도 신호 생성
    df.loc[triple_screen_buy | volatility_buy | trend_following_buy, "signal"] = 1
    df.loc[triple_screen_sell | volatility_sell | trend_following_sell, "signal"] = -1

    return df

