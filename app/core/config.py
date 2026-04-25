from dataclasses import dataclass
import os

@dataclass
class Config:
    api_key: str | None = os.getenv("BINANCE_API_KEY")
    api_secret: str | None = os.getenv("BINANCE_API_SECRET")
    mode: str = os.getenv("MODE", "paper")
    top_n: int = int(os.getenv("TOP_N", "5"))
    max_portfolio: int = int(os.getenv("MAX_PORTFOLIO", "5"))
    leverage: int = int(os.getenv("LEVERAGE", "20"))
    risk_per_trade: float = float(os.getenv("RISK_PER_TRADE", "0.005"))
    max_daily_loss: float = float(os.getenv("MAX_DAILY_LOSS", "0.02"))
    max_open_risk: float = float(os.getenv("MAX_OPEN_RISK", "0.03"))
    max_correlation: float = float(os.getenv("MAX_CORRELATION", "0.8"))
    min_quote_volume: float = float(os.getenv("MIN_QUOTE_VOLUME", "5000000"))
    max_spread_pct: float = float(os.getenv("MAX_SPREAD_PCT", "0.15"))
    ws_intervals: list[str] = os.getenv("WS_INTERVALS", "1m,5m,15m,1h,4h,1d").split(",")
    cache_ttl_days: int = int(os.getenv("CACHE_TTL_DAYS", "7"))
    retrain_days: int = int(os.getenv("RETRAIN_DAYS", "3"))
    confidence_half_life_days: int = int(os.getenv("CONFIDENCE_HALF_LIFE_DAYS", "7"))
