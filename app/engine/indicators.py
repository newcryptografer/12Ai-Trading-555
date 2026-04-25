import pandas as pd
import ta

def enrich(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["ema20"] = ta.trend.ema_indicator(df["close"], window=20)
    df["ema50"] = ta.trend.ema_indicator(df["close"], window=50)
    df["ema200"] = ta.trend.ema_indicator(df["close"], window=200)
    df["rsi"] = ta.momentum.rsi(df["close"], window=14)
    macd = ta.trend.macd(df["close"])
    signal = ta.trend.macd_signal(df["close"])
    df["macd_hist"] = macd - signal
    df["atr"] = ta.volatility.average_true_range(df["high"], df["low"], df["close"], window=14)
    df["bb_h"] = ta.volatility.bollinger_hband(df["close"], window=20)
    df["bb_l"] = ta.volatility.bollinger_lband(df["close"], window=20)
    df["bb_width"] = (df["bb_h"] - df["bb_l"]) / df["close"]
    df["roc"] = ta.momentum.roc(df["close"], window=10)
    df["vwap"] = (df["close"] * df["volume"]).cumsum() / df["volume"].cumsum()
    df["vol_sma"] = df["volume"].rolling(20).mean()
    df["rolling_high"] = df["high"].rolling(20).max()
    df["rolling_low"] = df["low"].rolling(20).min()
    df["zscore"] = (df["close"] - df["close"].rolling(20).mean()) / df["close"].rolling(20).std()
    return df.dropna().reset_index(drop=True)
