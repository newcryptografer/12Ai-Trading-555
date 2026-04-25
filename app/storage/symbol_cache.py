import json, time
from pathlib import Path

class SymbolCache:
    def __init__(self, path='output/symbol_cache.json', ttl_days=7, retrain_days=3):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl_days * 86400
        self.retrain = retrain_days * 86400
        self.data = self._load()

    def _load(self):
        if self.path.exists():
            return json.loads(self.path.read_text(encoding='utf-8'))
        return {}

    def save(self):
        self.path.write_text(json.dumps(self.data, indent=2), encoding='utf-8')

    def get(self, symbol):
        item = self.data.get(symbol)
        if not item:
            return None
        if time.time() - item.get('ts', 0) > self.ttl:
            return None
        return item

    def needs_retrain(self, symbol):
        item = self.data.get(symbol)
        if not item:
            return True
        return (time.time() - item.get('train_ts', 0)) > self.retrain

    def set(self, symbol, payload):
        payload = dict(payload)
        payload['ts'] = time.time()
        payload.setdefault('train_ts', time.time())
        self.data[symbol] = payload
        self.save()
