class ExitLogic:
    def should_exit(self, signal, current_price, trailing_stop=None):
        if signal.side == "LONG":
            if current_price >= signal.tp:
                return "tp_long"
            if trailing_stop is not None and current_price <= trailing_stop:
                return "trail_long"
            if current_price <= signal.sl:
                return "sl_long"
        else:
            if current_price <= signal.tp:
                return "tp_short"
            if trailing_stop is not None and current_price >= trailing_stop:
                return "trail_short"
            if current_price >= signal.sl:
                return "sl_short"
        return None
