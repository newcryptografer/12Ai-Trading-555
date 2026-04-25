from app.core.config import Config
from app.data.binance_client import BinanceClient
from app.engine.ensemble import EnsembleEngine
from app.main import build_frame


def test_ensemble():
    cfg = Config()
    client = BinanceClient()
    engine = EnsembleEngine(cfg)
    frames = {tf: build_frame() for tf in cfg.ws_intervals}
    sig = engine.evaluate_symbol("BTCUSDT", client, frames)
    assert sig.score >= 0
    assert 0 <= sig.confidence <= 1
