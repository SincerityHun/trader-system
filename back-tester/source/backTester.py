def backtest(df, initial_balance=10000):
    balance = initial_balance # 현금 상태
    position = 0  # 보유한 자산 수량 - 0이면 전부 현금
    last_price = 0 # 최근 매수가
    trade_history = [] # 실제 사고 판 내역

    for i in range(1, len(df)):
        if df["signal"].iloc[i] == 1 and position == 0: # 전량 매수
            position = balance / df["close"].iloc[i]
            balance = 0
            last_price = df["close"].iloc[i]
            trade_history.append(("buy", df["timestamp"].iloc[i], df["close"].iloc[i]))
        elif df["signal"].iloc[i] == -1 and position > 0: # 전량 매도
            balance = position * df["close"].iloc[i]
            position = 0
            print(
                f"Trade: Buy at {last_price}, Sell at {df['close'].iloc[i]}, Profit: {balance - initial_balance}"
            )
            trade_history.append(("sell", df["timestamp"].iloc[i], df["close"].iloc[i]))

    # calculate final balance
    final_balance = balance if balance > 0 else position * df["close"].iloc[-1]

    # calculate %
    return_pct = ((final_balance - initial_balance) / initial_balance) * 100
    print(f"Final Balance: {final_balance:.2f}")
    print(f"Return: {return_pct:.2f}%")
    return return_pct, trade_history