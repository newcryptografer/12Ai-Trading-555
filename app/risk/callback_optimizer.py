class CallbackOptimizer:
    def choose(self, symbol, atr_pct, confidence, regime, side):
        base = 0.8
        if atr_pct >= 0.03:
            base = 2.5
        elif atr_pct >= 0.02:
            base = 1.8
        elif atr_pct >= 0.01:
            base = 1.2
        else:
            base = 0.7
        if regime in {"trend", "momentum"}:
            base *= 0.9
        if regime == "breakout":
            base *= 1.15
        if confidence >= 0.85:
            base *= 0.85
        elif confidence <= 0.55:
            base *= 1.2
        if side == "SHORT":
            base *= 1.05
        return max(0.1, min(10.0, round(base, 2)))
