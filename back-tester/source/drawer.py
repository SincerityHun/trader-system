import plotly.graph_objects as go

def drawGraph(df,trade_history):
    fig = go.Figure()

    # 가격 데이터
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['close'], mode='lines', name='Price'))

    # 이동평균선 추가
    # fig.add_trace(go.Scatter(x=df['timestamp'], y=df['short_ma'], mode='lines', name='Short MA'))
    # fig.add_trace(go.Scatter(x=df['timestamp'], y=df['long_ma'], mode='lines', name='Long MA'))

    # 매수 / 매도 신호 추가
    # buy_signals = df[df['signal'] == 1]
    # sell_signals = df[df['signal'] == -1]

    # fig.add_trace(go.Scatter(
    #     x=buy_signals['timestamp'], y=buy_signals['close'], mode='markers',
    #     marker=dict(color='green', size=10, symbol='triangle-up'),
    #     name="Buy Signal"
    # ))

    # fig.add_trace(go.Scatter(
    #     x=sell_signals['timestamp'], y=sell_signals['close'], mode='markers',
    #     marker=dict(color='red', size=10, symbol='triangle-down'),
    #     name="Sell Signal"
    # ))

    # 실제 매매가 이루어진 지점만 추가
    buy_trades = [(t, p) for action, t, p in trade_history if action == "buy"]
    sell_trades = [(t, p) for action, t, p in trade_history if action == "sell"]

    if buy_trades:
        buy_times, buy_prices = zip(*buy_trades)
        fig.add_trace(
            go.Scatter(
                x=buy_times,
                y=buy_prices,
                mode="markers",
                marker=dict(color="green", size=12, symbol="triangle-up"),
                name="Buy Trades",
            )
        )

    if sell_trades:
        sell_times, sell_prices = zip(*sell_trades)
        fig.add_trace(
            go.Scatter(
                x=sell_times,
                y=sell_prices,
                mode="markers",
                marker=dict(color="red", size=12, symbol="triangle-down"),
                name="Sell Trades",
            )
        )
    fig.update_layout(
        title="Trading Strategy Backtest",
        xaxis_title="Time",
        yaxis_title="Price",
        hovermode="x",
        dragmode="zoom"
    )

    fig.show()
