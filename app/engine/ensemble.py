from app.core.models import CoinSignal
from app.engine.indicators import enrich

class EnsembleEngine:
    def __init__(self, cfg):
        self.cfg = cfg

    def evaluate_symbol(self, symbol, client, frames):
        total = 0.0
        votes = {}
        for tf, df in frames.items():
            if df is None or df.empty:
                continue
            edf = enrich(df)
            row = edf.iloc[-1]
            vote = self._vote(row, client, symbol)
            votes[tf] = vote
            total += vote["score"]
        confidence = min(1.0, total / 150.0)
        best_tf = max(votes, key=lambda k: votes[k]["score"]) if votes else "1m"
        strategy = votes[best_tf]["strategy"] if votes else "trend"
        entry = client.last_price(symbol)
        tp, sl = self._tp_sl(entry, strategy, confidence)
        allow_long = total > 40 and any(v["long_bias"] for v in votes.values())
        allow_short = total > 40 and any(v["short_bias"] for v in votes.values())
        side = "LONG" if allow_long else "SHORT"
        return CoinSignal(symbol, total, confidence, best_tf, strategy, entry, tp, sl, side, allow_long, allow_short, votes)

    def _vote(self, row, client, symbol):
        trend = 20 if row.ema20 > row.ema50 > row.ema200 else 5
        momentum = 15 if row.macd_hist > 0 and row.rsi > 50 else 5
        breakout = 20 if row.close >= row.rolling_high * 0.995 else 5
        mean_rev = 20 if row.rsi < 35 or row.rsi > 65 or abs(row.zscore) > 1.5 else 5
        volume = 10 if row.volume > row.vol_sma else 3
        volatility = 8 if row.atr > 0 else 2
        liquidity = 10 if client.liquid(symbol) else 1
        sentiment = client.sentiment_score(symbol)
        oi = client.oi_score(symbol)
        funding = client.funding_score(symbol)
        cvd = client.cvd_score(symbol)
        regime = client.regime_score(symbol)
        strat = max([("trend", trend), ("momentum", momentum), ("breakout", breakout), ("mean_reversion", mean_rev)], key=lambda x: x[1])[0]
        score = trend + momentum + breakout + mean_rev + volume + volatility + liquidity + sentiment + oi + funding + cvd + regime
        return {"score": score, "strategy": strat, "long_bias": strat in {"trend", "momentum", "breakout"}, "short_bias": strat == "mean_reversion" or funding < 0}

    def _tp_sl(self, entry, strategy, confidence, side):
        if side == "LONG":
            if strategy in {"trend", "momentum", "breakout"}:
                tp = entry * (1 + 0.02 + confidence * 0.02)
                sl = entry * (1 - 0.01 - (1 - confidence) * 0.01)
            else:
                tp = entry * 0.992
                sl = entry * 1.008
        else:
            if strategy in {"trend", "momentum", "breakout"}:
                tp = entry * (1 - 0.02 - confidence * 0.02)
                sl = entry * (1 + 0.01 + (1 - confidence) * 0.01)
            else:
                tp = entry * 1.008
                sl = entry * 0.992
        return tp, sl
