from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import atexit

class TradingAPSchedulerService:
    def __init__(self, warmup_fn, retrain_fn, health_fn=None, timezone="Europe/Istanbul"):
        self.warmup_fn = warmup_fn
        self.retrain_fn = retrain_fn
        self.health_fn = health_fn
        self.scheduler = BackgroundScheduler(timezone=timezone, job_defaults={"coalesce": True, "max_instances": 1, "misfire_grace_time": 300})

    def start(self):
        self.scheduler.add_job(self.warmup_fn, IntervalTrigger(hours=6), id="cache_warmup", replace_existing=True)
        self.scheduler.add_job(self.retrain_fn, CronTrigger(hour="3", minute="0"), id="symbol_retrain", replace_existing=True)
        if self.health_fn:
            self.scheduler.add_job(self.health_fn, IntervalTrigger(hours=4), id="health_check", replace_existing=True)
        self.scheduler.start()
        atexit.register(lambda: self.scheduler.shutdown(wait=False))
        return self

    def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
