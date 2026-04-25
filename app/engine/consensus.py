class ConsensusEngine:
    def decide(self, votes):
        if not votes:
            return {"signal": None, "reason": "no_votes", "confidence": 0.0}
        n = len(votes)
        buy_votes = sum(1 for v in votes.values() if v["long_bias"])
        sell_votes = sum(1 for v in votes.values() if v["short_bias"])
        if buy_votes == n:
            return {"signal": "BUY", "reason": "all_models_buy", "confidence": 1.0}
        if sell_votes == n:
            return {"signal": "SELL", "reason": "all_models_sell", "confidence": 1.0}
        return {"signal": None, "reason": "no_consensus", "confidence": 0.0}
