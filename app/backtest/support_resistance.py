import pandas as pd

class SupportResistanceBacktester:
    def find_zones(self, df, lookback=50, bins=20):
        prices = df["close"].tail(lookback)
        hist = pd.cut(prices, bins=bins).value_counts().sort_index()
        zones = []
        for interval, count in hist.items():
            if count >= max(2, int(lookback * 0.05)):
                zones.append({"low": float(interval.left), "high": float(interval.right), "touches": int(count)})
        return zones

    def predict_targets(self, df, side="LONG"):
        zones = self.find_zones(df)
        last = float(df["close"].iloc[-1])
        if not zones:
            return {"support": last * 0.98, "resistance": last * 1.02, "target": last * (1.03 if side == "LONG" else 0.97)}
        below = [z for z in zones if z["high"] < last]
        above = [z for z in zones if z["low"] > last]
        support = max(below, key=lambda z: z["high"])["high"] if below else last * 0.98
        resistance = min(above, key=lambda z: z["low"])["low"] if above else last * 1.02
        target = resistance * 0.995 if side == "LONG" else support * 1.005
        return {"support": support, "resistance": resistance, "target": target, "zones": zones}
