class PaperBroker:
    def __init__(self):
        self.orders = []

    def place_order(self, symbol, side, qty, price=None, meta=None):
        order = {"symbol": symbol, "side": side, "qty": qty, "price": price, "meta": meta or {}, "status": "FILLED_PAPER"}
        self.orders.append(order)
        return order
