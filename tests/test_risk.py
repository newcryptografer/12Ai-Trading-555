from app.core.config import Config
from app.core.models import CoinSignal
from app.risk.manager import RiskManager


def test_risk():
    cfg = Config()
    risk = RiskManager(cfg)
    sig = CoinSignal("BTCUSDT", 80, 0.8, "1h", "trend", 100, 105, 98, "LONG")
    assert risk.can_open(sig)
    assert risk.size(sig) > 0
