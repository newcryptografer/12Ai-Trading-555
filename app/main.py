import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from app.core.config import Config
from app.data.binance_client import BinanceClient
from app.data.scanner import Scanner
from app.engine.ensemble import EnsembleEngine
from app.risk.manager import RiskManager
from app.execution.rate_limit import RateLimitGuard
from app.execution.executor import Executor
from app.execution.portfolio import PortfolioManager


def build_frame(n=400):
    base = 100 + np.cumsum(np.random.normal(0, 1, n))
    high = base + np.abs(np.random.normal(0.4, 0.2, n))
    low = base - np.abs(np.random.normal(0.4, 0.2, n))
    open_ = np.r_[base[0], base[:-1]]
    volume = np.random.uniform(1000, 5000, n)
    return pd.DataFrame({"open_time": np.arange(n), "open": open_, "high": high, "low": low, "close": base, "volume": volume})


def main():
    cfg = Config()
    client = BinanceClient(cfg.api_key, cfg.api_secret)
    guard = RateLimitGuard()
    scanner = Scanner(client, cfg, guard)
    ensemble = EnsembleEngine(cfg)
    risk = RiskManager(cfg)
    dyn = DynamicRisk(cfg)
    cb = CallbackOptimizer()
    topt = TrailingOptimizer()
    wfo = WalkForwardOptimizer()
    sr = SupportResistanceBacktester()
    cache = SymbolCache(ttl_days=cfg.cache_ttl_days, retrain_days=cfg.retrain_days)
    decay = ConfidenceDecay(half_life_days=cfg.confidence_half_life_days)
    decision_engine = DecisionEngine()
    broker = PaperBroker()
    vol_filter = VolatilityFilter()
    warmup = CacheWarmupScheduler(cache, sr, lambda s: build_frame())
    retrainer = RetrainScheduler(cache, sr, lambda s: build_frame())
    scheduler_service = TradingAPSchedulerService(lambda: warmup.run_for_symbols(symbols), lambda: retrainer.run(symbols))
    executor = Executor(cfg, client)
    portfolio = PortfolioManager(cfg, executor, risk)
    consensus = ConsensusEngine()
    symbols = scanner.scan()
    def eval_symbol(sym):
        frames = {tf: build_frame() for tf in cfg.ws_intervals}
        return ensemble.evaluate_symbol(sym, client, frames)
    with ThreadPoolExecutor(max_workers=min(8, len(symbols) or 1)) as ex:
        ranked = list(ex.map(eval_symbol, symbols))
    ranked.sort(key=lambda x: x.score, reverse=True)
    final = []
    for sig in ranked:
        v = sig.meta
        if not v:
            continue
        if all(m.get("long_bias", False) for m in v.values()):
            sig.side = "LONG"
            sig.meta["dyn"] = dyn.levels(sig.entry, atr=1.5, confidence=sig.confidence, side="LONG", strategy=sig.strategy)
            sig.meta["callback_rate"] = cb.choose(sig.symbol, atr_pct=0.015, confidence=sig.confidence, regime=sig.strategy, side="LONG")
sig.meta["callback_rate"] = float(topt.best(sig.symbol, default=sig.meta["callback_rate"]))
            sig.tp = sig.meta["dyn"]["tp"]
            sig.sl = sig.meta["dyn"]["sl"]
            final.append(sig)
        elif all(m.get("short_bias", False) for m in v.values()):
            sig.side = "SHORT"
            sig.meta["dyn"] = dyn.levels(sig.entry, atr=1.5, confidence=sig.confidence, side="SHORT", strategy=sig.strategy)
            sig.meta["callback_rate"] = cb.choose(sig.symbol, atr_pct=0.015, confidence=sig.confidence, regime=sig.strategy, side="SHORT")
sig.meta["callback_rate"] = float(topt.best(sig.symbol, default=sig.meta["callback_rate"]))
            sig.tp = sig.meta["dyn"]["tp"]
            sig.sl = sig.meta["dyn"]["sl"]
            final.append(sig)
    positions = portfolio.rebalance(final)
    print({"approved": [x.symbol for x in final[:cfg.top_n]], "positions": list(positions.keys())})

if __name__ == "__main__":
    main()

# Decision engine should be wired into signal selection logic by combining regime, AI and SR scores.

# Volatility filter should be combined in the final decision flow.

# Paper mode executes simulated fills only.