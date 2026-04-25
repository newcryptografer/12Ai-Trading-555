from collections import defaultdict, deque
from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

class BinanceClient:
    def __init__(self, api_key=None, api_secret=None):
        self.rest = UMFutures(key=api_key, secret=api_secret) if api_key and api_secret else UMFutures()
        self.ws = None
        self.candle_cache = defaultdict(lambda: defaultdict(lambda: deque(maxlen=500)))
        self.book_cache = {}
        self._fallback = {"sentiment": 8, "oi": 8, "funding": 4, "cvd": 7, "regime": 8}

    def exchange_info(self): return self.rest.exchange_info()
    def ticker_24hr(self): return self.rest.ticker_24hr_price_change()
    def book_ticker(self, symbol): return self.rest.book_ticker(symbol=symbol)
    def funding_rate(self, symbol): return self.rest.funding_rate(symbol=symbol, limit=1)
    def open_interest(self, symbol): return self.rest.open_interest(symbol=symbol)
    def open_interest_hist(self, symbol, period="5m", limit=30): return self.rest.open_interest_hist(symbol=symbol, period=period, limit=limit)
    def set_leverage(self, symbol, leverage): return self.rest.change_leverage(symbol=symbol, leverage=leverage)
    def new_order(self, **kwargs): return self.rest.new_order(**kwargs)
    def klines(self, symbol, interval, limit=300): return self.rest.klines(symbol=symbol, interval=interval, limit=limit)
    def start_stream(self, symbols, intervals, on_message=None):
        self.ws = UMFuturesWebsocketClient(on_message=on_message or self._on_message, is_combined=True)
        streams = [f"{s.lower()}@kline_{iv}" for s in symbols for iv in intervals]
        self.ws.subscribe(streams)
    def stop(self):
        if self.ws: self.ws.stop(); self.ws = None
    def _on_message(self, _, msg): pass
    def sentiment_score(self, symbol): return self._fallback["sentiment"]
    def oi_score(self, symbol): return self._fallback["oi"]
    def funding_score(self, symbol): return self._fallback["funding"]
    def cvd_score(self, symbol): return self._fallback["cvd"]
    def regime_score(self, symbol): return self._fallback["regime"]
    def liquid(self, symbol): return True
    def last_price(self, symbol): return 100.0
