class Scanner:
    def __init__(self, client, cfg, guard=None):
        self.client = client
        self.cfg = cfg
        self.guard = guard

    def scan(self):
        info = self.client.exchange_info()
        tickers = self.client.ticker_24hr()
        tm = {t["symbol"]: t for t in tickers}
        out = []
        for s in info.get("symbols", []):
            if s.get("contractType") != "PERPETUAL" or s.get("quoteAsset") != "USDT" or s.get("status") != "TRADING":
                continue
            sym = s["symbol"]
            t = tm.get(sym)
            if not t:
                continue
            if float(t.get("quoteVolume", 0) or 0) < self.cfg.min_quote_volume:
                continue
            book = self.client.book_ticker(sym)
            bid = float(book.get("bidPrice", 0) or 0)
            ask = float(book.get("askPrice", 0) or 0)
            spread = ((ask - bid) / ((ask + bid) / 2)) * 100 if bid and ask else 999
            if spread > self.cfg.max_spread_pct:
                continue
            out.append(sym)
        return out
