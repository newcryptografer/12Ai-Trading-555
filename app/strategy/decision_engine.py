from dataclasses import dataclass

@dataclass
class Decision:
    score: float
    action: str
    reason: str

class DecisionEngine:
    def __init__(self, regime_w=0.45, ai_w=0.2, sr_w=0.2, vol_w=0.15, long_threshold=0.66, short_threshold=0.34):
        self.regime_w = regime_w
        self.ai_w = ai_w
        self.sr_w = sr_w
        self.vol_w = vol_w
        self.long_threshold = long_threshold
        self.short_threshold = short_threshold

    def normalize(self, x):
        return max(0.0, min(1.0, float(x)))

    def score(self, regime_score, ai_score, sr_score, vol_score):
        return (
            self.normalize(regime_score) * self.regime_w +
            self.normalize(ai_score) * self.ai_w +
            self.normalize(sr_score) * self.sr_w +
            self.normalize(vol_score) * self.vol_w
        )

    def decide(self, regime_score, ai_score, sr_score, vol_score):
        s = self.score(regime_score, ai_score, sr_score, vol_score)
        if s >= self.long_threshold:
            return Decision(s, 'LONG', 'high_confidence_alignment')
        if s <= self.short_threshold:
            return Decision(s, 'SHORT', 'low_confidence_alignment')
        return Decision(s, 'WAIT', 'mixed_signal')
