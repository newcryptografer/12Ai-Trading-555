class RiskManager:
    def __init__(self, cfg):
        self.cfg = cfg
        self.daily_loss = 0.0
        self.open_risk = 0.0

    def can_open(self, signal, correlation=0.0):
        if self.daily_loss >= self.cfg.max_daily_loss:
            return False
        if self.open_risk >= self.cfg.max_open_risk:
            return False
        if correlation >= self.cfg.max_correlation:
            return False
        return True

    def size(self, signal, atr=None):
        vol_adj = 1.0 if not atr else min(1.0, 1.0 / max(atr, 1e-6))
        return max(0.001, round(self.cfg.risk_per_trade * signal.confidence * signal.score / 100.0 * vol_adj, 6))

    def register_open(self, signal):
        self.open_risk += signal.confidence * 0.01

    def register_close(self, pnl_pct):
        if pnl_pct < 0:
            self.daily_loss += abs(pnl_pct)
