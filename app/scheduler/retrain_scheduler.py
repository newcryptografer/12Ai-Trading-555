from datetime import datetime

class RetrainScheduler:
    def __init__(self, cache, sr, fetch_frame):
        self.cache = cache
        self.sr = sr
        self.fetch_frame = fetch_frame

    def run(self, symbols):
        retrained = []
        for sym in symbols:
            if self.cache.needs_retrain(sym):
                df = self.fetch_frame(sym)
                res = self.sr.predict_targets(df, side='LONG')
                self.cache.set(sym, {**res, 'train_ts': datetime.utcnow().timestamp()})
                retrained.append(sym)
        return retrained
