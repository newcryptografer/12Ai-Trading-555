from dataclasses import dataclass, field
from typing import Any

@dataclass
class CoinSignal:
    symbol: str
    score: float
    confidence: float
    regime: str
    strategy: str
    entry: float
    tp: float
    sl: float
    side: str
    allow_long: bool = True
    allow_short: bool = True
    meta: dict[str, Any] = field(default_factory=dict)
