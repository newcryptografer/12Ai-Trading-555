class TrailingStopManager:
    def __init__(self):
        self.state = {}

    def update(self, symbol, side, price, trail):
        s = self.state.setdefault(symbol, {"best": price, "stop": None})
        if side == "LONG":
            s["best"] = max(s["best"], price)
            new_stop = s["best"] - trail
            s["stop"] = new_stop if s["stop"] is None else max(s["stop"], new_stop)
            return s["stop"]
        s["best"] = min(s["best"], price)
        new_stop = s["best"] + trail
        s["stop"] = new_stop if s["stop"] is None else min(s["stop"], new_stop)
        return s["stop"]
