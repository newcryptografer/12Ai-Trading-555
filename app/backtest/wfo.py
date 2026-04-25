import numpy as np

class WalkForwardOptimizer:
    def optimize_callback(self, symbol, df):
        returns = df["close"].pct_change().fillna(0)
        vol = float(returns.std()) if len(returns) else 0.01
        trend = float(returns.rolling(20).mean().iloc[-1]) if len(returns) > 20 else 0.0
        regime = "trend" if trend > 0 else "mean_reversion"
        base = 0.8
        if vol > 0.03:
            base = 2.5
        elif vol > 0.02:
            base = 1.8
        elif vol > 0.01:
            base = 1.2
        if regime == "trend":
            base *= 0.9
        score = float(np.clip(base + vol * 10, 0.1, 10.0))
        return {"callback_rate": round(score, 2), "regime": regime, "confidence": round(min(1.0, 0.5 + abs(trend) * 10), 2)}
