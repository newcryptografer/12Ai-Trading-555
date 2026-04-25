class ConfidenceDecay:
    def __init__(self, half_life_days=7):
        self.half_life = half_life_days * 86400

    def apply(self, base_confidence, age_seconds):
        if age_seconds <= 0:
            return base_confidence
        factor = 0.5 ** (age_seconds / self.half_life)
        return max(0.0, min(1.0, base_confidence * factor))
