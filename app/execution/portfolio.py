class PortfolioManager:
    def __init__(self, cfg, executor, risk):
        self.cfg = cfg
        self.executor = executor
        self.risk = risk
        self.positions = {}

    def rebalance(self, ranked):
        target = ranked[: self.cfg.max_portfolio]
        target_symbols = {x.symbol for x in target}
        for sym in list(self.positions.keys()):
            if sym not in target_symbols:
                pos = self.positions.pop(sym)
                self.executor.close(sym, pos["signal"].side, pos["qty"])
                self.risk.register_close(-0.001)
        for sig in target:
            if sig.symbol not in self.positions and self.risk.can_open(sig):
                qty = self.risk.size(sig)
                self.executor.set_leverage(sig.symbol)
                self.positions[sig.symbol] = {"signal": sig, "qty": qty, "order": self.executor.open(sig, qty)}
                self.risk.register_open(sig)
        return self.positions
