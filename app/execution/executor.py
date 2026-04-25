class Executor:
    def __init__(self, cfg, client):
        self.cfg = cfg
        self.client = client

    def set_leverage(self, symbol):
        return self.client.set_leverage(symbol, self.cfg.leverage) if self.cfg.mode == "live" else {"paper": True, "symbol": symbol}

    def open(self, signal, qty):
        if self.cfg.mode == "live":
            side = "BUY" if signal.side == "LONG" else "SELL"
            return self.client.new_order(symbol=signal.symbol, side=side, type="MARKET", quantity=qty)
        return {"paper": "open", "symbol": signal.symbol, "side": signal.side, "qty": qty, "tp": signal.tp, "sl": signal.sl}

    def close(self, symbol, side, qty):
        if self.cfg.mode == "live":
            close_side = "SELL" if side == "LONG" else "BUY"
            return self.client.new_order(symbol=symbol, side=close_side, type="MARKET", quantity=qty, reduceOnly=True)
        return {"paper": "close", "symbol": symbol, "side": side, "qty": qty}
