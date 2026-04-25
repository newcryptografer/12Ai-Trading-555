class DynamicRisk:
    def __init__(self, cfg):
        self.cfg = cfg

    def levels(self, entry, atr, confidence, side, strategy):
        atr = max(float(atr or 0), 1e-8)
        base_mult = 1.2 if strategy in {"trend", "momentum", "breakout"} else 0.9
        tp_mult = base_mult + confidence * 1.2
        sl_mult = 0.8 + (1 - confidence) * 0.9
        trail_mult = 0.9 + confidence * 0.6
        if side == "LONG":
            tp = entry + atr * tp_mult
            sl = entry - atr * sl_mult
            trail = atr * trail_mult
        else:
            tp = entry - atr * tp_mult
            sl = entry + atr * sl_mult
            trail = atr * trail_mult
        return {"tp": tp, "sl": sl, "trail": trail}
