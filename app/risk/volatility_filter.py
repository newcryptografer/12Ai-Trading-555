class VolatilityFilter:
    def __init__(self, low=0.008, high=0.03):
        self.low = low
        self.high = high

    def score(self, df):
        r = df["close"].pct_change().dropna()
        if len(r) == 0:
            return 0.5, "neutral"
        vol = float(r.std())
        if vol < self.low:
            return 0.35, "low"
        if vol > self.high:
            return 0.65, "high"
        return 0.5, "normal"
