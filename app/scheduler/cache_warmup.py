from datetime import datetime

class CacheWarmupScheduler:
    def __init__(self, cache, sr, fetch_frame):
        self.cache = cache
        self.sr = sr
        self.fetch_frame = fetch_frame

    def run_for_symbols(self, symbols):
        updated = []
        for sym in symbols:
            df = self.fetch_frame(sym)
            res = self.sr.predict_targets(df, side='LONG')
            self.cache.set(sym, {**res, 'train_ts': datetime.utcnow().timestamp()})
            updated.append(sym)
        return updated
