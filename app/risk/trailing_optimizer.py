import json
from pathlib import Path

class TrailingOptimizer:
    def __init__(self, path='output/callback_stats.json'):
        self.path = Path(path)
        self.stats = self._load()

    def _load(self):
        if self.path.exists():
            return json.loads(self.path.read_text(encoding='utf-8'))
        return {}

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.stats, indent=2), encoding='utf-8')

    def update(self, symbol, callback_rate, pnl_pct):
        s = self.stats.setdefault(symbol, {"candidates": {}})
        c = s["candidates"].setdefault(str(callback_rate), {"trades": 0, "wins": 0, "pnl": 0.0})
        c["trades"] += 1
        if pnl_pct > 0:
            c["wins"] += 1
        c["pnl"] += pnl_pct
        self._save()

    def best(self, symbol, default=1.0):
        s = self.stats.get(symbol, {})
        cands = s.get("candidates", {})
        if not cands:
            return default
        return max(cands.items(), key=lambda kv: (kv[1]["pnl"], kv[1]["wins"], kv[1]["trades"]))[0]
